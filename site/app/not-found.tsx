import Link from "next/link";

export default function NotFound() {
  return (
    <main className="status-page">
      <span className="brand__mark" aria-hidden="true">
        ))
      </span>
      <p>404 · outside the catalog</p>
      <h1>This page is not part of the atlas.</h1>
      <Link className="button button--primary" href="/">
        Return to FRB Atlas
      </Link>
    </main>
  );
}
