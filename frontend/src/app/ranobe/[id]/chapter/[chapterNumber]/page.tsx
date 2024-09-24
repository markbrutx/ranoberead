'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useSwipeable } from 'react-swipeable';

interface Chapter {
  id: number;
  ranobe_id: number;
  chapter_id: number;
  chapter_number_origin: number;
  title_ru: string;
  title_en: string;
  content_ru: string;
  content_en: string | null;
}

async function getChapterContent(
  ranobeId: string,
  chapterId: string
): Promise<Chapter> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/chapters/${ranobeId}/${chapterId}?lang=ru`
  );
  if (!res.ok) {
    throw new Error('Failed to fetch chapter content');
  }
  return res.json();
}

async function createBookmark(ranobeId: string, chapterId: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/bookmarks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json' // Указываем правильный Content-Type
    },
    body: JSON.stringify({
      ranobe_id: parseInt(ranobeId),
      chapter_id: parseInt(chapterId)
    })
  });
  if (!res.ok) {
    throw new Error('Failed to create bookmark');
  }
  return res.json();
}

function formatContent(content: string) {
  const paragraphs = content.split('\n');
  return paragraphs.map((paragraph, index) => (
    <p key={index} className="mb-4">
      {paragraph}
    </p>
  ));
}

export default function ChapterPage({
  params
}: {
  params: { id: string; chapterNumber: string };
}) {
  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [bookmarkStatus, setBookmarkStatus] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    setError(null);
    getChapterContent(params.id, params.chapterNumber)
      .then((data) => {
        setChapter(data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching chapter:', err);
        setError(err.message);
        setIsLoading(false);
      });
  }, [params.id, params.chapterNumber]);

  const handlers = useSwipeable({
    onSwipedLeft: () => {
      // Navigate to next chapter
      if (chapter) {
        window.location.href = `/ranobe/${params.id}/chapter/${
          chapter.chapter_id + 1
        }`;
      }
    },
    onSwipedRight: () => {
      // Navigate to previous chapter
      if (chapter) {
        window.location.href = `/ranobe/${params.id}/chapter/${
          chapter.chapter_id - 1
        }`;
      }
    }
  });

  const handleCreateBookmark = async () => {
    try {
      await createBookmark(params.id, params.chapterNumber);
      setBookmarkStatus('Bookmark created successfully!');
      setTimeout(() => setBookmarkStatus(null), 3000);
    } catch (err) {
      setBookmarkStatus('Failed to create bookmark. Please try again.');
      setTimeout(() => setBookmarkStatus(null), 3000);
    }
  };

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

  if (!chapter) return null;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4" {...handlers}>
      <header className="mb-8 relative">
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="absolute top-0 right-0 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Menu
        </button>
        <h1 className="text-2xl font-bold mb-4">
          {chapter.chapter_number_origin} - {chapter.title_ru || 'Без названия'}
        </h1>
        <Link
          href={`/ranobe/${params.id}`}
          className="text-blue-400 hover:text-blue-300 inline-block"
        >
          Back to Chapters
        </Link>
        {isMenuOpen && (
          <div className="absolute top-12 right-0 bg-gray-800 p-4 rounded-lg shadow-lg">
            <button
              onClick={handleCreateBookmark}
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full mb-2"
            >
              Create Bookmark
            </button>
            <button
              onClick={() => setIsMenuOpen(false)}
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded w-full"
            >
              Close Menu
            </button>
          </div>
        )}
        {bookmarkStatus && (
          <div className="mt-4 p-2 bg-blue-500 text-white rounded">
            {bookmarkStatus}
          </div>
        )}
      </header>
      <article className="max-w-prose mx-auto">
        <div className="mt-4 leading-relaxed text-gray-200 text-lg">
          {formatContent(chapter.content_ru)}
        </div>
      </article>
      <footer className="mt-8 flex justify-between">
        <Link
          href={`/ranobe/${params.id}/chapter/${chapter.chapter_id - 1}`}
          className="text-blue-400 hover:text-blue-300"
        >
          Previous Chapter
        </Link>
        <Link
          href={`/ranobe/${params.id}/chapter/${chapter.chapter_id + 1}`}
          className="text-blue-400 hover:text-blue-300"
        >
          Next Chapter
        </Link>
      </footer>
    </div>
  );
}
