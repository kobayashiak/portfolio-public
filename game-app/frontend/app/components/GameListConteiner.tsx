"use client"

import { useEffect, useState, } from "react";
import {useRouter,usePathname,useSearchParams} from 'next/navigation'
import SearchBox from "./SearchBox";
import GameList from "./GameList"
import PageNumber from "./PageNumber"
import { FirstModal } from "./FirstModal";
import {Game} from '../types/game'
import { url } from "../url";



interface SortOption{
      value:string;
      sort:string;
    }

    interface Option{
      value:string;
      column:string;
    }

    export interface TotalCount{
      totalCount:number;
      max_page:number;
    }

    export interface SearchForm{
      word:string,
      selectedOption:string,
      selectedSortOption:string,
      page:number;
    }

    export const sortOptions:SortOption[] = [
        {value:'true',sort:'昇順'},
        {value:'false',sort:'降順'}
    ]

    export const options: Option[] = [
        {value:'0',column:'ゲーム名'},
        {value:'1',column:'実績取得率'},
    ]

export const GameListContainer=() => {

  

    const[games,setGames] = useState<Game[]>([])

    const[searchForm,setSearchForm] = useState<SearchForm>({
      word:"",
      selectedOption:options[0].value,
      selectedSortOption:sortOptions[0].value,
      page:1
    })

    const[totalCount,setTotalCount] = useState<TotalCount>({totalCount:0,max_page:0})

    const router = useRouter()
    const pathname = usePathname()
    const searchParams = useSearchParams()

    const handleSearch = (overridePage?:number) =>{
        try{
            const currentPath = pathname;
            const params = new URLSearchParams(searchParams);
            params.set('freeword',searchForm.word);
            params.set('order',searchForm.selectedSortOption);
            params.set('column',searchForm.selectedOption);
            
            params.set('page',(overridePage !== undefined? overridePage:1).toString())

            router.push(`${currentPath}?${params.toString()}`)
            
        }catch(error){
            console.error("エラー:",error)
        }
    }

    useEffect(()=>{
      console.log('動いた！')

      const fetchData = async () =>{
        try{
        const query = searchParams.toString();

        const response = await fetch (`${url}/games${query? `?${query}` : ''}`);
        if(!response.ok) throw new Error("通信失敗")
        const data = await response.json();
        setGames(data.items);
        setTotalCount({totalCount:data.totalCount,max_page:data.max_page})
        window.scrollTo(0, 0);
        }catch(error){
          console.error("fetchエラー",error);
        }

      }
      fetchData();

                    },[searchParams])

  return (
      <div className='relative'>
      <FirstModal/>
      <div className="flex flex-col gap-10">
        <div className="mb-6 border-l-2 border-sky-600 py-1 pl-2">
        <p className="text-[10px] text-slate-500 font-black uppercase tracking-[0.3em] leading-none mb-1.5">
          Application Service / System
        </p>
        <h2 className="text-xs text-slate-300 font-bold tracking-widest">
        所持ゲーム一覧
        </h2>
        </div>
        <section className="w-full">
          <SearchBox  searchForm={searchForm} setSearchForm = {setSearchForm} handleSearch = {handleSearch}/>
        </section>
        <section className="w-full">
          <GameList games = {games}/>
        </section>
        <section className="w-full py-6 border-t border-slate-800/50">
          <PageNumber searchForm={searchForm} totalCount={totalCount} setSearchForm={setSearchForm} handleSearch={handleSearch}/>
        </section>
      </div>

      </div>
  );
}