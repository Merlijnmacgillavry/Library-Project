import React, { createContext, useState } from 'react'

export default function SearchProvider(props: any) {

   const [results, setResults] = useState({})

  function search(query: string): any {
    fetch('http://localhost:5000/search?' + new URLSearchParams({
        query: query,
        page: '1'
    })).then((response) => {
        response.json().then((value) => {
           setResults(value)
           console.log(value)
        })
    }).catch((e) =>{
        return null
    })
  }

  return (
    <SearchContext.Provider value={{search, results}}>{props.children}</SearchContext.Provider>
  )
}
export const SearchContext = createContext<SearchContent>({
    search:(_query: string)=>{}, 
    results: {}
})

export type SearchContent = {
    search:(query: string) => any,
    results: Object
}