import Link from 'next/link';

async function getRanobeList() {
  const res = await fetch('http://localhost:5000/ranobe');
  if (!res.ok) {
    throw new Error('Failed to fetch ranobe list');
  }
  return res.json();
}

export default async function Home() {
  const ranobeList = await getRanobeList();

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-2xl font-bold mb-4">Ranobe List</h1>
      <ul>
        {ranobeList.map((ranobe: any) => (
          <li key={ranobe.id} className="mb-2">
            <Link
              href={`/ranobe/${ranobe.id}`}
              className="text-blue-400 hover:text-blue-300"
            >
              {ranobe.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
