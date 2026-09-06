import { createFileRoute } from "@tanstack/react-router";
import { PageShell } from "@/components/layout/site-header";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export const Route = createFileRoute("/architecture")({
  component: ArchitecturePage,
});

const LAYERS = [
  {
    title: "Handlers",
    files: "app/handlers/customer.py · admin.py · errors.py",
    body: "Thin Telegram adapters. They parse updates, answer callbacks, and call services. No SQL lives here.",
  },
  {
    title: "Services",
    files: "lead · export · notification · validation · auth",
    body: "Lead creation, duplicate window, status transitions, CSV bytes, admin checks, and outbound notices.",
  },
  {
    title: "Repositories",
    files: "app/repositories/lead_repository.py",
    body: "The only module that talks to SQLAlchemy for leads: create, fetch, list, counts, notes, duplicates.",
  },
  {
    title: "Persistence",
    files: "SQLAlchemy 2 async · aiosqlite · Alembic",
    body: "UTC timestamps, enum columns without native PG enums, human-readable public_id, SQLite for the local demo.",
  },
];

function ArchitecturePage() {
  return (
    <PageShell>
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <Badge variant="muted">Python bot</Badge>
        <h1 className="mt-4 max-w-3xl font-display text-4xl italic tracking-tight">
          Modular on purpose — handlers stay thin.
        </h1>
        <p className="mt-4 max-w-2xl text-sm leading-relaxed text-muted sm:text-base">
          The interactive preview you are using is a faithful CRM model. The
          portfolio artifact is the Python package: aiogram 3, tests, Docker,
          and Alembic. Both share the same lead shape and status vocabulary.
        </p>

        <div className="mt-10 grid gap-4 md:grid-cols-2">
          {LAYERS.map((layer) => (
            <Card key={layer.title} className="p-6">
              <h2 className="text-base font-semibold">{layer.title}</h2>
              <p className="mt-2 font-mono text-xs text-primary">{layer.files}</p>
              <p className="mt-3 text-sm leading-relaxed text-muted">
                {layer.body}
              </p>
            </Card>
          ))}
        </div>

        <Card className="mt-8 p-6">
          <h2 className="text-base font-semibold">Lead fields</h2>
          <p className="mt-2 font-mono text-xs leading-relaxed text-muted">
            id · public_id · telegram_user_id · username · full_name · phone ·
            service_category · description · preferred_contact_method · status
            · admin_note · created_at · updated_at
          </p>
        </Card>
      </div>
    </PageShell>
  );
}
