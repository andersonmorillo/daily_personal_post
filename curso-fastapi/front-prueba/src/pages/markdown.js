import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'
import React from 'react';
import ReactMarkdown from 'react-markdown';
import { fetchMarkdownContent } from '../utils/api';

const inter = Inter({ subsets: ['latin'] })


function MarkdownPage({ markdownContent }) {
  return (
    <div className={`${styles.main} ${inter.className}`}>
      <ReactMarkdown>{markdownContent}</ReactMarkdown>
    </div>
  );
}

export async function getServerSideProps() {
  const markdownContent = await fetchMarkdownContent();
  return { props: { markdownContent } };
}

export default MarkdownPage;