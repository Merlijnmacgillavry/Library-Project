import React, { createContext, useEffect, useState } from 'react'

export default function SearchProvider(props: any) {

  const [results, setResults] = useState<SearchResult[]>([])
  const [lastQuery, setLastQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const [models, setModels] = useState<string[]>([])
  const [currentModel, setCurrentModel] = useState("tfidf")
  const [currentPage, setCurrentPage] = useState(1)

  useEffect(() => {
    loadModels()
  }, [])

  useEffect(() => {
    if (results.length > 0) {
      setLoading(false)
    }
  }, [results])

  useEffect(() => {
    if (models.length > 0) {
      setLoading(false)
    }
  }, [models])

  function loadModels(): void {
    setLoading(true)
    fetch('http://localhost:5000/models').then((response) => {
      response.json().then((value) => {
        setModels(value)
        console.log(value)
      })
    }).catch((e) => {
      console.log(e)
    })

  }


  function search(query: string): any {
    setLoading(true)
    fetch('http://localhost:5000/search?' + new URLSearchParams({
      query: query,
      page: currentPage.toString(),
      model: currentModel
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
    if (lastQuery !== "") {
      fetch('http://localhost:5000/search?' + new URLSearchParams({
        query: lastQuery,
        page: page.toString(),
        model: currentModel
      })).then((response) => {
        response.json().then((value: SearchResult[]) => {
          setResults(value)
          setCurrentPage(page)
          console.log(value)
        })
      }).catch((e) => {
        console.log(e)
      })
    } else {
      setCurrentPage(page)
      setLoading(false)

    }

  }

  function getProfile(uuid: string): SearchResult | void {
    if (results.length > 0) {
      const found_results = results.filter(res => res.uuid === uuid)
      if (found_results.length > 0) {
        return found_results[0]
      }
    }
  }

  function changeModel(model: string): void {
    setLoading(true)
    if (lastQuery !== "") {
      fetch('http://localhost:5000/search?' + new URLSearchParams({
        query: lastQuery,
        page: currentPage.toString(),
        model: model
      })).then((response) => {
        response.json().then((value: SearchResult[]) => {
          setResults(value)
          setCurrentModel(model)
        })
      }).catch((e) => {
        console.log(e)
      })
    } else {
      setCurrentModel(model)
      setLoading(false)
    }

  }

  return (
    <SearchContext.Provider value={{ search, results, lastQuery, changePage, loading, models, changeModel, currentModel, currentPage, getDocument: getProfile }}>{props.children}</SearchContext.Provider>
  )
}
export const SearchContext = createContext<SearchContent>({
  search: (_query: string) => { },
  results: [],
  lastQuery: "",
  changePage: (_page: number) => { },
  changeModel: (_model: string) => { },
  loading: false,
  models: [],
  currentModel: "tfidf",
  currentPage: 1,
  getDocument: (_uuid: string) => { }
})

export type SearchContent = {
  search: (query: string) => void,
  results: SearchResult[],
  lastQuery: string,
  changePage: (page: number) => void,
  loading: boolean,
  models: string[],
  changeModel: (_model: string) => void,
  currentModel: string
  currentPage: number
  getDocument: (uuid: string) => SearchResult | void
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