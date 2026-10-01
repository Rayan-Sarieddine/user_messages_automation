"use client";

import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";

import { submitTriage } from "@/lib/api";
import { SOURCES, Source, TriageRecord, TriageRequest } from "@/lib/types";

interface TriageFormProps {
  onResult: (record: TriageRecord) => void;
}

export function TriageForm({ onResult }: TriageFormProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TriageRequest>({
    defaultValues: { source: "Email", message: "" },
  });

  const mutation = useMutation({
    mutationFn: submitTriage,
    onSuccess: (record) => {
      onResult(record);
      reset({ source: "Email", message: "" });
    },
  });

  const onSubmit = (data: TriageRequest) => mutation.mutate(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex w-full flex-col gap-4">
      <div className="flex flex-col gap-1.5">
        <label htmlFor="source" className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
          Source
        </label>
        <select
          id="source"
          className="rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
          {...register("source", { required: true })}
        >
          {SOURCES.map((source: Source) => (
            <option key={source} value={source}>
              {source}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="message" className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
          Message
        </label>
        <textarea
          id="message"
          rows={6}
          placeholder="Paste the raw customer message here..."
          className="rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
          {...register("message", { required: "A message is required", minLength: 3 })}
        />
        {errors.message && (
          <p className="text-sm text-red-600 dark:text-red-400">{errors.message.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={mutation.isPending}
        className="self-start rounded-md bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-300"
      >
        {mutation.isPending ? "Processing..." : "Submit for triage"}
      </button>

      {mutation.isError && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {mutation.error instanceof Error ? mutation.error.message : "Something went wrong."}
        </p>
      )}
    </form>
  );
}
