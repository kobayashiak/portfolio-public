import { Achievement } from "@/app/types/game"

interface Props{
achievement:Achievement

}

export const AchievementListItem =({achievement}:Props)=> {

            const isUnlocked = achievement.unlocktime > 0;

            const formatDate = (unixTime:number) =>{
                if(unixTime === 0)return "未取得";
                const date = new Date(unixTime*1000);
                return date.toLocaleDateString("ja-JP",{
                    year:"numeric",
                    month:"2-digit",
                    day:"2-digit",
                    hour:"2-digit",
                    minute:"2-digit",
                })
            };


            return(<div>
                        <div className={`p-5 rounded-xl border transition-all duration-200 ${isUnlocked ? "bg-slate-800 border-slate-700 shadow-md hover:border-blue-500":
                            "bg-slate-900 border-slate-800 opacity-60"}`}>
                                <div className="flex justify-between items-start mb-3">
                                <h3 className="text-lg font-bold text-white leading-tight">
                                {achievement.display_name}</h3>
                                <span>
                                <span className="text-xs">グローバル実績取得率:</span>
                                <span className="text-xs font-mono bg-blue-900/50 text-blue-300 px-2 py-1 rounded">
                                {achievement.percent.toFixed(1)}%
                                </span>
                                </span>
                                </div>
                                <div className="text-sm text-slate-300 mb-4 min-h-5">
                                    {achievement.description ? (achievement.description)
                                     : (<span className="text-slate-500 italic text-xs">
                                        （詳細条件は非公開です）
                                        </span>
        )}
                                </div>
                                <div className="flex items-center gap-2 mt-auto pt-3 border-t border-slate-700/50">
                                <span className="text-[10px] uppercase tracking-wider text-slate-500 font-semibold">
                                    Status
                                    </span>
                                    <span className={`text-xs ${isUnlocked ? "text-green-400" : "text-slate-500"}`}>
                                        {formatDate(achievement.unlocktime)}
                                    </span>

                                </div>

                                </div>
                   </div>)
}