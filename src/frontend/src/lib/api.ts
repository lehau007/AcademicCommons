const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean | undefined>;
}

async function request<T>(
  method: string,
  endpoint: string,
  body?: unknown,
  options: RequestOptions = {}
): Promise<T> {
  const { params, headers, ...restOptions } = options;

  // Construct URL with query parameters
  let url = `${BASE_URL}${endpoint}`;
  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null) {
        searchParams.append(key, String(val));
      }
    });
    const queryString = searchParams.toString();
    if (queryString) {
      url += `?${queryString}`;
    }
  }

  // Get token from localStorage
  let token: string | null = null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('token');
  }

  // Set default headers
  const defaultHeaders: Record<string, string> = {};

  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  // Do not set Content-Type if body is FormData
  const isFormData = body instanceof FormData;
  if (!isFormData && body) {
    defaultHeaders['Content-Type'] = 'application/json';
  }

  const mergedHeaders = {
    ...defaultHeaders,
    ...headers,
  } as HeadersInit;

  const config: RequestInit = {
    method,
    headers: mergedHeaders,
    ...restOptions,
  };

  if (body) {
    config.body = isFormData ? (body as BodyInit) : JSON.stringify(body);
  }

  let response: Response;
  try {
    response = await fetch(url, config);
  } catch {
    // Network-level failure (server unreachable, CORS, connection reset).
    throw new Error(
      `Không thể kết nối tới máy chủ (${method} ${endpoint}). Vui lòng kiểm tra kết nối hoặc thử lại.`
    );
  }

  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status}`;
    try {
      const errorJson = await response.json();
      const detail = errorJson.detail ?? errorJson.message;
      if (Array.isArray(detail)) {
        // FastAPI validation errors: detail is an array of {loc, msg, ...} objects
        errorMessage = detail
          .map((e) => (typeof e === 'object' && e?.msg ? e.msg : String(e)))
          .join('; ');
      } else if (typeof detail === 'string') {
        errorMessage = detail;
      } else if (detail) {
        errorMessage = JSON.stringify(detail);
      }
    } catch {
      // ignore JSON parse error for error responses that aren't JSON
    }
    const e = new Error(errorMessage) as Error & { status?: number };
    e.status = response.status;
    throw e;
  }

  // If response is empty (e.g. 204 No Content), return empty or null
  if (response.status === 204) {
    return {} as T;
  }

  // Try to parse as JSON, otherwise text, otherwise empty
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json() as Promise<T>;
  } else {
    const text = await response.text();
    return text as unknown as T;
  }
}

// ---------------------------------------------------------------------------
// Virtual Tutor streaming (SSE over POST)
// ---------------------------------------------------------------------------
// EventSource cannot send a POST body or an Authorization header, so we stream
// the response manually with fetch + ReadableStream and parse `data:` lines.

export interface TutorStreamPayload {
  course_code: string;
  question: string;
  session_id?: string;
  document_ids?: string[];
}

export interface TutorStreamHandlers {
  onSession?: (sessionId: string) => void;
  onStatus?: (step: string, label: string) => void;
  onTextDelta?: (text: string) => void;
  onReset?: () => void;
  onDone?: (data: { session_id: string; answer: string; citations?: unknown[] }) => void;
  onError?: (message: string) => void;
}

export async function streamTutorQuery(
  payload: TutorStreamPayload,
  handlers: TutorStreamHandlers
): Promise<void> {
  let token: string | null = null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('token');
  }

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Accept: 'text/event-stream',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let response: Response;
  try {
    response = await fetch(`${BASE_URL}/tutor/query/stream`, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });
  } catch {
    handlers.onError?.(
      'Không thể kết nối tới máy chủ AI Tutor. Vui lòng kiểm tra kết nối hoặc thử lại.'
    );
    return;
  }

  if (!response.ok || !response.body) {
    let message = `HTTP error! status: ${response.status}`;
    try {
      const errorJson = await response.json();
      const detail = errorJson.detail ?? errorJson.message;
      if (typeof detail === 'string') {
        message = detail;
      }
    } catch {
      // non-JSON error body; keep the status-based message
    }
    handlers.onError?.(message);
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  const dispatch = (raw: string) => {
    // Each SSE event may carry one or more `data:` lines; concatenate them.
    const dataLines = raw
      .split('\n')
      .filter((line) => line.startsWith('data:'))
      .map((line) => line.slice(5).trimStart());
    if (dataLines.length === 0) return;

    let event: Record<string, unknown>;
    try {
      event = JSON.parse(dataLines.join('\n')) as Record<string, unknown>;
    } catch {
      return; // ignore malformed event
    }

    const str = (v: unknown): string => (typeof v === 'string' ? v : '');

    switch (event.type) {
      case 'session':
        handlers.onSession?.(str(event.session_id));
        break;
      case 'status':
        handlers.onStatus?.(str(event.step), str(event.label));
        break;
      case 'text_delta':
        handlers.onTextDelta?.(str(event.text));
        break;
      case 'reset':
        handlers.onReset?.();
        break;
      case 'done':
        handlers.onDone?.({
          session_id: str(event.session_id),
          answer: str(event.answer),
          citations: Array.isArray(event.citations) ? event.citations : undefined,
        });
        break;
      case 'error':
        handlers.onError?.(str(event.message) || 'Đã xảy ra lỗi khi xử lý câu hỏi.');
        break;
      default:
        break;
    }
  };

  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      // Events are separated by a blank line. Buffer partial chunks across reads.
      let sepIndex: number;
      while ((sepIndex = buffer.indexOf('\n\n')) !== -1) {
        const rawEvent = buffer.slice(0, sepIndex);
        buffer = buffer.slice(sepIndex + 2);
        if (rawEvent.trim()) {
          dispatch(rawEvent);
        }
      }
    }
    // Flush any trailing event that wasn't terminated by a blank line.
    if (buffer.trim()) {
      dispatch(buffer);
    }
  } catch {
    handlers.onError?.('Kết nối tới AI Tutor bị gián đoạn. Vui lòng thử lại.');
  }
}

export const api = {
  get: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>('GET', endpoint, undefined, options),

  post: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    request<T>('POST', endpoint, body, options),

  put: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    request<T>('PUT', endpoint, body, options),

  patch: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    request<T>('PATCH', endpoint, body, options),

  del: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    request<T>('DELETE', endpoint, body, options),
};

export default api;
