'use client';

import Link from 'next/link';
import { useCallback, useEffect, useRef, useState } from 'react';
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

const BookmarkIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
  </svg>
);

export default function ChapterPage({
  params
}: {
  params: { id: string; chapterNumber: string };
}) {
  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isBookmarkVisible, setIsBookmarkVisible] = useState(true);
  const [bookmarkStatus, setBookmarkStatus] = useState<string | null>(null);
  const lastInteractionTime = useRef(Date.now());
  const hideTimeout = useRef<NodeJS.Timeout | null>(null);

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
      if (chapter) {
        window.location.href = `/ranobe/${params.id}/chapter/${
          chapter.chapter_id + 1
        }`;
      }
    },
    onSwipedRight: () => {
      if (chapter) {
        window.location.href = `/ranobe/${params.id}/chapter/${
          chapter.chapter_id - 1
        }`;
      }
    },
    trackMouse: true
  });

  const handleCreateBookmark = async () => {
    try {
      await createBookmark(params.id, params.chapterNumber);
      setBookmarkStatus('Закладка создана успешно!');
    } catch (error) {
      console.error('Ошибка при создании закладки:', error);
      setBookmarkStatus('Не удалось создать закладку. Попробуйте еще раз.');
    } finally {
      setTimeout(() => setBookmarkStatus(null), 3000);
    }
  };

  const handleInteraction = useCallback(() => {
    lastInteractionTime.current = Date.now();
    setIsBookmarkVisible(true);
    if (hideTimeout.current) {
      clearTimeout(hideTimeout.current);
    }
    hideTimeout.current = setTimeout(() => {
      if (Date.now() - lastInteractionTime.current >= 3000) {
        setIsBookmarkVisible(false);
      }
    }, 3000);
  }, []);

  useEffect(() => {
    const events = ['mousemove', 'scroll', 'click', 'touchstart', 'keydown'];
    events.forEach((event) => {
      window.addEventListener(event, handleInteraction);
    });

    return () => {
      events.forEach((event) => {
        window.removeEventListener(event, handleInteraction);
      });
      if (hideTimeout.current) {
        clearTimeout(hideTimeout.current);
      }
    };
  }, [handleInteraction]);

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
            Повторить
          </button>
        </div>
      </div>
    );
  }

  if (!chapter) return null;

  return (
    <div
      className="min-h-screen bg-gray-900 text-white p-4 relative"
      {...handlers}
    >
      <header className="mb-8">
        <h1 className="text-2xl font-bold mb-4">
          {chapter.chapter_number_origin} - {chapter.title_ru || 'Без названия'}
        </h1>
        <Link
          href={`/ranobe/${params.id}`}
          className="text-blue-400 hover:text-blue-300 inline-block"
        >
          Назад к главам
        </Link>
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
          Предыдущая глава
        </Link>
        <Link
          href={`/ranobe/${params.id}/chapter/${chapter.chapter_id + 1}`}
          className="text-blue-400 hover:text-blue-300"
        >
          Следующая глава
        </Link>
      </footer>

      {/* Floating Bookmark Button */}
      <button
        onClick={handleCreateBookmark}
        aria-label="Создать закладку"
        className={`fixed bottom-4 right-4 bg-blue-500 hover:bg-blue-700 text-white rounded-full p-3 shadow-lg transition-opacity duration-300 focus:outline-none focus:ring-2 focus:ring-blue-300 ${
          isBookmarkVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
      >
        <BookmarkIcon />
      </button>

      {/* Bookmark Status Toast */}
      {bookmarkStatus && (
        <div
          role="status"
          aria-live="polite"
          className="fixed bottom-20 right-4 bg-gray-800 text-white p-3 rounded shadow-lg transition-opacity duration-300"
        >
          {bookmarkStatus}
        </div>
      )}
    </div>
  );
}
