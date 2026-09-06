import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight } from "lucide-react";
import { PageShell } from "@/components/layout/site-header";
import { ChatDemo } from "@/components/telegram/chat-demo";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/demo")({ component: DemoPage });

function DemoPage() {
  return (
    <PageShell>
      <div className="mx-auto grid max-w-6xl gap-10 px-4 py-10 sm:px-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
        <div className="lg:sticky lg:top-24">
          <Badge variant="muted">Customer role</Badge>
          <h1 className="mt-4 font-display text-4xl italic tracking-tight">
            Submit a brief the way a customer would.
          </h1>
          <p className="mt-4 text-sm leading-relaxed text-muted sm:text-base">
            This screen mirrors the Telegram conversation implemented in the
            Python bot: a finite-state form, confirmation, duplicate
            protection, and a personal request list. Confirmed leads appear on
            the admin desk immediately.
          </p>
          <ol className="mt-6 space-y-3 text-sm text-muted">
            <li>1. Submit a request and complete every field.</li>
            <li>2. Review the summary — confirm, edit, or cancel.</li>
            <li>3. Open My requests to see the lead number and status.</li>
            <li>4. Switch to the admin desk to triage it.</li>
          </ol>
          <Button asChild className="mt-8" variant="secondary">
            <Link to="/desk">
              Continue to the desk
              <ArrowRight />
            </Link>
          </Button>
        </div>
        <ChatDemo />
      </div>
    </PageShell>
  );
}
