import React, { useContext, useState } from 'react'
import { Card, Pagination, Stack } from '@mantine/core';
import { SearchContext } from '../providers/SearchProvider';
import SearchResultCard from './SearchResultCard';

export default function SearchResults() {
  const { changePage, results } = useContext(SearchContext)

  const [activePage, setPage] = useState(1);
  //   return <Pagination value={activePage} onChange={setPage} total={10} />;
  return (
    <Stack>
      {results.map((data: SearchResultT, i: number) => {
        return <SearchResultCard key={i} data={data} />
      })}

    </Stack>
  )
}

export type SearchResultT = {
  uuid: string
  "repository link": string
  title: string
  author: string
  contributor: string
  "publication year": number
  abstract: string
  "subject topic": string
  language: string
  "publication type": string
  publisher: any
  isbn: any
  issn: any
  patent: any
  "patent status": any
  "bibliographic note": any
  "access restriction": any
  "embargo date": any
  faculty: any
  department: any
  "research group": any
  programme: string
  project: any
  coordinates: any
}

