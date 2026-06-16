export function ComingSoon({ title }: { title: string }) {
  return (
    <div className="flex h-full min-h-[60vh] flex-col items-center justify-center rounded-2xl border border-dashed border-neutral-300 bg-white p-12 text-center dark:border-neutral-700 dark:bg-neutral-900">
      <h2 className="text-lg font-semibold text-neutral-900 dark:text-neutral-50">
        {title}
      </h2>
      <p className="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
        Próximamente
      </p>
    </div>
  );
}
