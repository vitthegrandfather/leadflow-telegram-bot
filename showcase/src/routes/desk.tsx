import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/layout/site-header";
import { LeadDesk } from "@/components/desk/lead-desk";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/desk")({ component: DeskPage });

function DeskPage() {
  return (
    <PageShell>
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <Badge variant="muted">Administrator role</Badge>
        <h1 className="mt-4 font-display text-4xl italic tracking-tight">
          The /admin desk, without Telegram chrome.
        </h1>
        <p className="mt-4 max-w-2xl text-sm leading-relaxed text-muted sm:text-base">
          Sample leads are fictional. In the Python bot this surface is
          restricted to Telegram user IDs listed in ADMIN_IDS. Status changes
          can notify the customer; notes stay internal.
        </p>
        <div className="mt-8">
          <LeadDesk />
        </div>
      </div>
    </PageShell>
  );
}
