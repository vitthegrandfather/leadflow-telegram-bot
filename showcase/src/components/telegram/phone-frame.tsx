import type { ReactNode } from "react";

export function PhoneFrame({ children }: { children: ReactNode }) {
  return (
    <div className="mx-auto w-full max-w-[380px]">
      <div className="rounded-2xl bg-elevated p-2.5 shadow-[var(--shadow-float)]">
        <div className="relative overflow-hidden rounded-xl bg-bg">
          <div className="flex items-center justify-between px-5 pt-3 pb-2">
            <span className="font-mono text-[11px] text-muted tabular-nums">
              09:41
            </span>
            <span className="h-4 w-20 rounded-full bg-elevated" />
            <span className="flex gap-1">
              <span className="h-2 w-4 rounded-sm bg-muted/50" />
              <span className="h-2 w-2 rounded-sm bg-muted/80" />
            </span>
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
