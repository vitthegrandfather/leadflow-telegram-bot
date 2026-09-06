import type { LeadStatus } from "./types";

export const STATUS_BADGE: Record<
  LeadStatus,
  "muted" | "primary" | "ok" | "danger"
> = {
  new: "muted",
  in_progress: "primary",
  completed: "ok",
  cancelled: "danger",
};
