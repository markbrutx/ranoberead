'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

interface Chapter {
  id: number;
  chapter_id: number;
  chapter_number_origin: number;
  title_ru: string;
  title_en: string;
  content_preview_ru: string;
  content_preview_en: string;
}

interface RanobeDetails {
  id: number;
  title: string;
  chapter_count: number;
  chapters: Chapter[];
}

async function getRanobeDetails(id: string): Promise<RanobeDetails> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ranobe/${id}`);
  if (!res.ok) {
    throw new Error('Failed to fetch ranobe details');
  }
  return res.json();
}

export default function RanobePage({ params }: { params: { id: string } }) {
  const [ranobe, setRanobe] = useState<RanobeDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    getRanobeDetails(params.id)
      .then((data) => {
        setRanobe(data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching ranobe details:', err);
        setError(err.message);
        setIsLoading(false);
      });
  }, [params.id]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!ranobe) {
    return <div>No data available</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-2xl font-bold mb-4">{ranobe.title}</h1>
      <p>Chapter Count: {ranobe.chapter_count}</p>
      <Link
        href="/"
        className="text-blue-400 hover:text-blue-300 mb-4 inline-block"
      >
        Back to List
      </Link>
      <ul>
        {ranobe.chapters.map((chapter) => (
          <li key={chapter.id} className="mb-2">
            <Link
              href={`/ranobe/${ranobe.id}/chapter/${chapter.chapter_id}`}
              className="text-blue-400 hover:text-blue-300"
            >
              {chapter.chapter_number_origin} -{' '}
              {chapter.title_ru || 'Без названия'}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
