'use client'
import React, { useEffect,useState,use } from "react";
import { GameDetail } from "../types/game";
import {fetchDetail} from '../lib/api'
import { AchievementList } from "../games/[id]/components/AchievementList";
import { TagList } from "../games/[id]/components/TagList";
import { RecommendedGameCardList } from "../games/[id]/components/RecomendGameCardList";
import {SteamLinkCard} from "../games/[id]/components/SteamLinkCard";

interface Props{
    gameDetail :GameDetail;
    id:string;
}



export const GameDetailComponent = ({gameDetail,id}:Props)=>{
    const [gameDetailData,setGameDetail] = useState<GameDetail>(gameDetail);
    const [loading,setLoading] = useState(false);
    const [error,setError] = useState("");

    useEffect(()=>{
        const buildPage = async ()=>{
        if(id != String(gameDetailData.game.id)){
            setLoading(true);
                try{
                        setGameDetail(await fetchDetail(id));
                }catch(err){
                    if(err instanceof Error){
                        setError(err.message);
                    }else{
                        setError(String(err))
                    }
                    
                }finally{
                    setLoading(false);
                }
            }       
        }
            
        buildPage();
    },[id])

    if(loading || !gameDetailData) return<div>只今ロード中</div>;

    if(error != "") return <div>エラー発生：{error}</div>;


    return(
    <div className="space-y-12">
        <div className="mb-6 border-l-2 border-sky-600 py-1 pl-2">
        <p className="text-[10px] text-slate-500 font-black uppercase tracking-[0.3em] leading-none mb-1.5">
          Application Service / System
        </p>
        <h2 className="text-xs text-slate-300 font-bold tracking-widest">
        ゲーム詳細画面
        </h2>
        </div>
        
        <header className="space-y-2 border-l-4 border-sky-500 pl-6 py-2"><h1 className="text-4xl md:text-5xl font-black text-white italic tracking-tighter drop-shadow-md">
        {gameDetailData.game.name}</h1>
        <div className="flex items-baseline gap-2 text-slate-400 font-mono text-sm"><span className="tracking-widest text-xs">プレイ時間:</span>
        <span className="time">{Math.floor(gameDetailData.playtime / 60)}</span>
        <span className="timescale">時間</span>
        <span className="time">{gameDetailData.playtime % 60}</span>
        <span className="timescale">分</span>
        </div>
        </header>
    <p  className = 'whitespace-pre-wrap'>{gameDetailData.description}</p>
    {gameDetailData.game.is_owned==0 ? <SteamLinkCard id={gameDetailData.game.id}/>:<AchievementList achievements={gameDetailData.achievements}/>}
    <TagList tags={gameDetailData.tags}/>
    <RecommendedGameCardList recommendGames={gameDetailData.recommend_games}/>
    
    </div>)
}