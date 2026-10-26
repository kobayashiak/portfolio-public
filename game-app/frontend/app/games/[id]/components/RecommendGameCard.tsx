import { Game } from "@/app/types/game"
import  Link from "next/link"


interface Props{
    game:Game
}

export const RecommendedGameCard = ({game}:Props)=>{
    return(
            <Link href ={`/games/${game.id}`}>
                <div className = 'bg-gray-800/40 hover:bg-gray-700/60 border border-gray-700 rounded-lg p-4 transition-all duration-200 group'>
                    <h4 className="font-bold text-white truncate mb-2 group-hover:text-blue-400">{game.name}</h4>
                    <div className ="flex item-center justify-between">
                        <span className="text-sm font-mono text-green-400">{game.complete_rate}%</span>

                    </div>
                    <div className='w-full bg-gray-900 h-1.5 rounded-full mt-2 overflow-hidden'>
                        <div className='bg-green-500 h-full rounded-full transition-all' style={{width:`${game.complete_rate}%`}}/>
                    </div>
                </div>

            
            
            </Link>


    

    )
}