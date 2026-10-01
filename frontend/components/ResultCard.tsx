import { TriageRecord } from "@/lib/types";

const PRIORITY_STYLES: Record<string, string> = {
  Low: "bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300",
  Medium: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300",
  High: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300",
};

function Badge({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${className}`}
    >
      {children}
    </span>
  );
}

export function ResultCard({ record }: { record: TriageRecord }) {
  return (
    <div className="flex w-full flex-col gap-4 rounded-lg border border-zinc-200 bg-white p-5 dark:border-zinc-800 dark:bg-zinc-900">
      {record.escalation_flag && (
        <div className="rounded-md border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-800 dark:bg-red-950/40 dark:text-red-300">
          <strong>Escalated for human review.</strong> {record.escalation_reason}
        </div>
      )}

      <div className="flex flex-wrap items-center gap-2">
        <Badge className="bg-zinc-100 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-200">
          {record.category}
        </Badge>
        <Badge className={PRIORITY_STYLES[record.priority]}>{record.priority} priority</Badge>
        <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300">
          Routed to {record.routing_queue}
        </Badge>
        <Badge className="bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400">
          Confidence {Math.round(record.confidence * 100)}%
        </Badge>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Summary</h3>
        <p className="mt-1 text-sm text-zinc-700 dark:text-zinc-300">{record.summary}</p>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Core issue</h3>
        <p className="mt-1 text-sm text-zinc-700 dark:text-zinc-300">{record.core_issue}</p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Identifiers</h3>
          {record.identifiers.length > 0 ? (
            <ul className="mt-1 flex flex-wrap gap-1.5">
              {record.identifiers.map((id) => (
                <li
                  key={id}
                  className="rounded bg-zinc-100 px-2 py-0.5 text-xs font-mono text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300"
                >
                  {id}
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-1 text-sm text-zinc-500">None found</p>
          )}
        </div>

        <div>
          <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
            Urgency signal
          </h3>
          <p className="mt-1 text-sm text-zinc-700 dark:text-zinc-300">{record.urgency_signal}</p>
        </div>
      </div>

      <p className="text-xs text-zinc-400">
        Record {record.id} · {record.source} · {new Date(record.created_at).toLocaleString()}
      </p>
    </div>
  );
}
