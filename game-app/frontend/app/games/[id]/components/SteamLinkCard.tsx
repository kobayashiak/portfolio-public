
interface Props{
    id:number
}



export const SteamLinkCard =({id}:Props)=>{
    const link = 'https://store.steampowered.com/app/'+id
    return(<div className="p-4 border border-slate-700 bg-slate-900 rounded-lg shadow-xl mb-4">
        <div className="text-xs text-slate-400 mb-2 uppercase tracking-wider font-semibold">
        Not Owned
        </div>
        
        <a target="_blank" rel="noopener noreferrer" href = {link} className="
          group
          flex items-center justify-between
          p-5
          rounded-md
          /* Steamグラデーション (通常時) */
          bg-linear-to-r from-[#1b2838] to-[#2a475e]
          border border-[#417a9b]/30
          
          /* ホバー時のエフェクト: 少し明るく、青い光を纏わせる */
          hover:from-[#2a475e] hover:to-[#3a5a78]
          hover:border-[#66c0f4]
          hover:shadow-[0_0_20px_rgba(102,192,244,0.5)]
          
          transition-all duration-300 ease-in-out
          transform hover:-translate-y-0.5
          
          no-underline
          cursor-pointer">商品ページ</a></div>)
}