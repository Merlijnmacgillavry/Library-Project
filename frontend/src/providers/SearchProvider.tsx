import React, { createContext, useEffect, useState } from 'react'

export default function SearchProvider(props: any) {

  const [results, setResults] = useState<SearchResult[]>([])
  const [lastQuery, setLastQuery] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (results.length > 0) {
      setLoading(false)
    }
  }, [results])

  function search(query: string): any {
    setLoading(true)
    fetch('http://localhost:5000/search?' + new URLSearchParams({
      query: query,
      page: '1'
    })).then((response) => {
      response.json().then((value) => {
        setResults(value)
        setLastQuery(query)
        console.log(value)
      })
    }).catch((e) => {
      console.log(e)
    })
  }

  function changePage(page: number): void {
    setLoading(true)

    fetch('http://localhost:5000/search?' + new URLSearchParams({
      query: lastQuery,
      page: page.toString()
    })).then((response) => {
      response.json().then((value: SearchResult[]) => {
        setResults(value)
        console.log(value)
      })
    }).catch((e) => {
      console.log(e)
    })
  }

  return (
    <SearchContext.Provider value={{ search, results, lastQuery, changePage, loading }}>{props.children}</SearchContext.Provider>
  )
}
export const SearchContext = createContext<SearchContent>({
  search: (_query: string) => { },
  results: [],
  lastQuery: "",
  changePage: (_page: number) => { },
  loading: false
})

export type SearchContent = {
  search: (query: string) => void,
  results: SearchResult[],
  lastQuery: string,
  changePage: (page: number) => void,
  loading: boolean
}

export type SearchResult = {
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