export function formatDate(date: string) {
  return new Date(date)
    .toLocaleDateString("ko-KR", {
      year: "2-digit",
      month: "2-digit",
      day: "2-digit",
    })
    .replace(/\. /g, ".")
    .slice(0, -1);
}
