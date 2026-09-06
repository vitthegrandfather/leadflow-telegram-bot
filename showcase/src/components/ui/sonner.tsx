import { Toaster as Sonner } from "sonner";

export function Toaster() {
  return (
    <Sonner
      theme="dark"
      position="bottom-right"
      toastOptions={{
        classNames: {
          toast: "bg-elevated text-fg border-border shadow-[var(--shadow-float)]",
          description: "text-muted",
          actionButton: "bg-primary text-primary-fg",
        },
      }}
    />
  );
}
