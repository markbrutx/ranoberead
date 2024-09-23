// src/app/ranobe/[id]/chapter/[chapterNumber]/page.tsx
'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useSwipeable } from 'react-swipeable';

async function getChapterContent(ranobeId: string, chapterNumber: string) {
  const res = await fetch(
    `http://localhost:5000/chapters/${ranobeId}/${chapterNumber}`
  );
  if (!res.ok) {
    throw new Error('Failed to fetch chapter content');
  }
  return res.json();
}

function formatContent(content: string) {
  // Разбиваем текст на параграфы
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
  const [chapter, setChapter] = useState<any>(null);

  useEffect(() => {
    getChapterContent(params.id, params.chapterNumber).then(setChapter);
  }, [params.id, params.chapterNumber]);

  const handlers = useSwipeable({
    onSwipedLeft: () => {
      // Navigate to next chapter
    },
    onSwipedRight: () => {
      // Navigate to previous chapter
    }
  });

  if (!chapter)
    return (
      <div className="min-h-screen bg-gray-900 text-white p-4 flex items-center justify-center">
        Loading...
      </div>
    );

  const content = chapter.content_ru || chapter.content_en;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4" {...handlers}>
      <header className="mb-8">
        <h1 className="text-2xl font-bold mb-4">
          Chapter {params.chapterNumber}
        </h1>
        <Link
          href={`/ranobe/${params.id}`}
          className="text-blue-400 hover:text-blue-300 inline-block"
        >
          Back to Chapters
        </Link>
      </header>
      <article className="max-w-prose mx-auto">
        <div className="mt-4 leading-relaxed text-gray-200 text-lg">
          {formatContent(content)}
        </div>
      </article>
      <footer className="mt-8 flex justify-between">
        <Link
          href={`/ranobe/${params.id}/chapter/${
            parseInt(params.chapterNumber) - 1
          }`}
          className="text-blue-400 hover:text-blue-300"
        >
          Previous Chapter
        </Link>
        <Link
          href={`/ranobe/${params.id}/chapter/${
            parseInt(params.chapterNumber) + 1
          }`}
          className="text-blue-400 hover:text-blue-300"
        >
          Next Chapter
        </Link>
      </footer>
    </div>
  );
}
