import * as Dialog from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Sheet({
  open,
  onOpenChange,
  children,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: ReactNode;
}) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      {children}
    </Dialog.Root>
  );
}

export function SheetContent({
  children,
  className,
  title,
}: {
  children: ReactNode;
  className?: string;
  title: string;
}) {
  return (
    <Dialog.Portal>
      <Dialog.Overlay className="fixed inset-0 z-40 bg-bg/70 data-[state=open]:animate-in" />
      <Dialog.Content
        className={cn(
          "fixed inset-y-0 right-0 z-50 flex w-full max-w-lg flex-col bg-surface shadow-[var(--shadow-float)]",
          "border-l border-border",
          "data-[state=open]:translate-x-0",
          className,
        )}
      >
        <div className="flex items-center justify-between border-b border-border px-5 py-4">
          <Dialog.Title className="text-sm font-medium tracking-wide text-muted uppercase">
            {title}
          </Dialog.Title>
          <Dialog.Close className="inline-flex size-11 items-center justify-center rounded-md text-muted hover:bg-elevated hover:text-fg">
            <X className="size-4" />
            <span className="sr-only">Close</span>
          </Dialog.Close>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto p-5">{children}</div>
      </Dialog.Content>
    </Dialog.Portal>
  );
}
