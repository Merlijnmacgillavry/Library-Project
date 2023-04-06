import React, { createContext, useState } from 'react'

export default function SearchProvider(props: any) {

  const [results, setResults] = useState<SearchResult[]>([])
  const [lastQuery, setLastQuery] = useState("")

  function search(query: string): any {
    fetch('http://localhost:5000/search?' + new URLSearchParams({
        query: query,
        page: '1'
    })).then((response) => {
        response.json().then((value) => {
           setResults(value)
           setLastQuery(query)
           console.log(value)
        })
    }).catch((e) =>{
        console.log(e)
    })
  }

  function changePage(page: number): void{
    fetch('http://localhost:5000/search?' + new URLSearchParams({
      query: lastQuery,
      page: page.toString()
  })).then((response) => {
      response.json().then((value: SearchResult[]) => {
         setResults(value)
         console.log(value)
      })
  }).catch((e) =>{
      console.log(e)
  })
  }

  return (
    <SearchContext.Provider value={{search, results, lastQuery, changePage}}>{props.children}</SearchContext.Provider>
  )
}
export const SearchContext = createContext<SearchContent>({
    search:(_query: string)=>{}, 
    results: [], 
    lastQuery: "", 
    changePage:(_page:number)=>{}
})

export type SearchContent = {
    search:(query: string) => void,
    results: SearchResult[],
    lastQuery: string,
    changePage:(page: number)=> void,
}

export type SearchResult={
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