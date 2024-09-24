'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

interface Ranobe {
  id: number;
  title: string;
  chapter_count: number;
}

interface Bookmark {
  id: number;
  ranobe_id: number;
  chapter_id: number;
  ranobe_title: string;
  chapter_title_ru: string;
  chapter_number_origin: number;
}

async function getRanobeList(): Promise<Ranobe[]> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ranobe`);
  if (!res.ok) {
    throw new Error('Failed to fetch ranobe list');
  }
  return res.json();
}

async function getBookmarksList(): Promise<Bookmark[]> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/bookmarks`);
  if (!res.ok) {
    throw new Error('Failed to fetch bookmarks list');
  }
  return res.json();
}

export default function Home() {
  const [ranobeList, setRanobeList] = useState<Ranobe[]>([]);
  const [bookmarksList, setBookmarksList] = useState<Bookmark[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      setIsLoading(true);
      setError(null);

      try {
        const [ranobeData, bookmarksData] = await Promise.all([
          getRanobeList(),
          getBookmarksList()
        ]);
        setRanobeList(ranobeData);
        setBookmarksList(bookmarksData);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError((err as Error).message || 'Failed to fetch data');
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white p-4 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 text-white p-4 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-3xl font-bold mb-8 text-center">Ranobe Reader</h1>

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-2xl font-bold mb-4">Ranobe List</h2>
          <ul className="space-y-2">
            {ranobeList.map((ranobe) => (
              <li key={ranobe.id} className="bg-gray-800 p-3 rounded-lg">
                <Link
                  href={`/ranobe/${ranobe.id}`}
                  className="text-blue-400 hover:text-blue-300"
                >
                  {ranobe.title} ({ranobe.chapter_count} chapters)
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h2 className="text-2xl font-bold mb-4">Bookmarks</h2>
          {bookmarksList.length > 0 ? (
            <ul className="space-y-2">
              {bookmarksList.map((bookmark) => (
                <li key={bookmark.id} className="bg-gray-800 p-3 rounded-lg">
                  <Link
                    href={`/ranobe/${bookmark.ranobe_id}/chapter/${bookmark.chapter_id}`}
                    className="text-blue-400 hover:text-blue-300"
                  >
                    <span className="font-semibold">
                      {bookmark.ranobe_title}
                    </span>
                    <br />
                    <span className="text-sm text-gray-400">
                      Chapter {bookmark.chapter_number_origin}:{' '}
                      {bookmark.chapter_title_ru}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-400">No bookmarks yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
