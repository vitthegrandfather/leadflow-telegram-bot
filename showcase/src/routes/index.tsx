import { createFileRoute, Link } from "@tanstack/react-router";
import {
  ArrowRight,
  ClipboardList,
  Lock,
  MessageSquare,
  ShieldCheck,
} from "lucide-react";
import { PageShell } from "@/components/layout/site-header";
import { ChatDemo } from "@/components/telegram/chat-demo";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  return (
    <PageShell>
      <section className="border-b border-border">
        <div className="mx-auto grid max-w-6xl gap-12 px-4 py-12 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:py-20">
          <div>
            <Badge variant="primary">Portfolio demonstration</Badge>
            <h1 className="mt-5 font-display text-4xl leading-[1.1] tracking-tight italic sm:text-5xl lg:text-6xl">
              Telegram intake
              <span className="block not-italic text-muted">
                for a small studio desk.
              </span>
            </h1>
            <p className="mt-5 max-w-xl text-base leading-relaxed text-muted sm:text-lg">
              LeadFlow Bot collects structured customer requests in Telegram
              and hands them to an administrator with status, notes, and CSV
              export. This preview is an interactive model of the Python bot —
              not paid client work.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Button asChild size="lg">
                <Link to="/demo">
                  Try the customer flow
                  <ArrowRight />
                </Link>
              </Button>
              <Button asChild size="lg" variant="secondary">
                <Link to="/desk">Open the admin desk</Link>
              </Button>
            </div>
            <p className="mt-5 font-mono text-xs tracking-wide text-subtle">
              Python 3.12 · aiogram 3 · SQLAlchemy 2 · SQLite
            </p>
          </div>
          <div className="lg:justify-self-end">
            <ChatDemo compact />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <p className="text-xs tracking-[0.2em] text-muted uppercase">
          What it covers
        </p>
        <h2 className="mt-3 font-display text-3xl italic">
          A complete lead path, not a toy /start handler.
        </h2>
        <div className="mt-10 grid gap-4 md:grid-cols-2">
          <Feature
            icon={MessageSquare}
            title="Customer conversation"
            body="Welcome, menu, five-step brief, confirmation with edit/cancel, human-readable lead numbers, and a personal request list."
          />
          <Feature
            icon={ClipboardList}
            title="Administrator desk"
            body="Counts by status, recent leads, full detail, status changes, internal notes, customer notifications, and CSV export."
          />
          <Feature
            icon={Lock}
            title="Admin-only access"
            body="Administrator commands and callbacks are gated by Telegram user IDs from the environment. Unknown users never see lead data."
          />
          <Feature
            icon={ShieldCheck}
            title="Production-minded defaults"
            body="Validation, phone normalisation, HTML escaping, duplicate protection, structured logs, Alembic migrations, tests, and Docker."
          />
        </div>
      </section>
    </PageShell>
  );
}

function Feature({
  icon: Icon,
  title,
  body,
}: {
  icon: typeof MessageSquare;
  title: string;
  body: string;
}) {
  return (
    <Card className="p-6">
      <Icon className="size-5 text-primary" />
      <h3 className="mt-4 text-base font-semibold">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted">{body}</p>
    </Card>
  );
}
