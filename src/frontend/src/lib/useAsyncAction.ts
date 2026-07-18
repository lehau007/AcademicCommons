import { useCallback, useRef, useState } from "react";

/**
 * Wraps an async handler so it cannot run again while a previous call is still
 * in flight. The `inFlight` ref is checked and set synchronously, so it blocks
 * rapid double-clicks that fire before React re-renders the disabled button —
 * something `disabled={loading}` state alone cannot guarantee.
 *
 * Usage:
 *   const { pending, run } = useAsyncAction(async () => { await api.post(...); });
 *   <button onClick={run} disabled={pending}>Submit</button>
 */
export function useAsyncAction<A extends unknown[]>(
  fn: (...args: A) => Promise<void>
): { pending: boolean; run: (...args: A) => Promise<void> } {
  const [pending, setPending] = useState(false);
  const inFlight = useRef(false);

  const run = useCallback(
    async (...args: A) => {
      if (inFlight.current) return;
      inFlight.current = true;
      setPending(true);
      try {
        await fn(...args);
      } finally {
        inFlight.current = false;
        setPending(false);
      }
    },
    [fn]
  );

  return { pending, run };
}
