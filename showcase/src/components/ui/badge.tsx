import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium tracking-wide",
  {
    variants: {
      variant: {
        default: "border-transparent bg-elevated text-fg",
        primary: "border-transparent bg-primary/15 text-primary",
        muted: "border-border bg-transparent text-muted",
        ok: "border-transparent bg-ok/15 text-ok",
        danger: "border-transparent bg-danger/15 text-danger",
        outline: "border-border text-fg",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export function Badge({
  className,
  variant,
  ...props
}: React.HTMLAttributes<HTMLSpanElement> & VariantProps<typeof badgeVariants>) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}
