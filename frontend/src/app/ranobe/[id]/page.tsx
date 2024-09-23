import Link from 'next/link';

const CHAPTER_START = 337;
const CHAPTER_COUNT = 5;

async function getRanobeDetails(id: string) {
  const res = await fetch(`http://localhost:5000/ranobe/${id}`);
  if (!res.ok) {
    throw new Error('Failed to fetch ranobe details');
  }
  return res.json();
}

export default async function RanobePage({
  params
}: {
  params: { id: string };
}) {
  const ranobe = await getRanobeDetails(params.id);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-2xl font-bold mb-4">{ranobe.title}</h1>
      <Link
        href="/"
        className="text-blue-400 hover:text-blue-300 mb-4 inline-block"
      >
        Back to List
      </Link>
      <ul>
        {[...Array(CHAPTER_COUNT)].map((_, index) => (
          <li key={index} className="mb-2">
            <Link
              href={`/ranobe/${ranobe.id}/chapter/${CHAPTER_START + index}`}
              className="text-blue-400 hover:text-blue-300"
            >
              Chapter {CHAPTER_START + index}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
