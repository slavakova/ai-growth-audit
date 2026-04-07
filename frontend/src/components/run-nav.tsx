import Link from "next/link";

export function RunNav({ runId }: { runId: string }) {
  const items = [
    { href: `/runs/${runId}`, label: "Summary" },
    { href: `/runs/${runId}/competitors`, label: "Competitors" },
    { href: `/runs/${runId}/comparison`, label: "Comparison" },
    { href: `/runs/${runId}/recommendations`, label: "Recommendations" },
    { href: `/runs/${runId}/assets`, label: "Generated assets" },
  ];

  return (
    <div className="mb-4 flex flex-wrap gap-2">
      {items.map((item) => (
        <Link key={item.href} href={item.href} className="rounded border px-3 py-1 text-sm hover:bg-slate-100">
          {item.label}
        </Link>
      ))}
    </div>
  );
}
