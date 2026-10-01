"use client";

import { useState } from "react";

import { ResultCard } from "@/components/ResultCard";
import { TriageForm } from "@/components/TriageForm";
import { TriageRecord } from "@/lib/types";

export default function Home() {
  const [result, setResult] = useState<TriageRecord | null>(null);

  return (
    <div className="flex flex-1 justify-center bg-zinc-50 px-6 py-16 dark:bg-black">
      <main className="flex w-full max-w-xl flex-col gap-8">
        <div>
          <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-50">
            ArcVault Intake &amp; Triage
          </h1>
          <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
            Submit a raw inbound customer message to classify, enrich, and route it
            automatically.
          </p>
        </div>

        <TriageForm onResult={setResult} />

        {result && <ResultCard record={result} />}
      </main>
    </div>
  );
}
