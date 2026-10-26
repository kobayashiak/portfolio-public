
'use client'
import { useRouter,useSearchParams,usePathname } from "next/navigation"

export const FirstModal = ()=>{

    const router = useRouter()
    const searchParams = useSearchParams()
    const pathName = usePathname()

    const modalStatus = searchParams.get("checked_modal")

    const tapOKButton = ()=>{
        const params = new URLSearchParams(searchParams)
        const currentPath = pathName
        params.set("checked_modal","checked")
        router.replace(`${currentPath}?${params.toString()}`)
    }


    return(modalStatus !=="checked" && <div className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/50'>
            <div className="bg-white p-8 rounded-lg max-w-md shadow-xl text-center">
                <h2 className="text-xl text-black font-bold mb-4">このサイトについて</h2>
                <p className="mb-6 text-black">これは、ゲームの実績を管理、解析し、次に購入するゲームをお勧めするサイトです。<br/>OKボタンを押し、検索を始めてください！</p>

            
            <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-amber-700 transition-all" onClick={()=>tapOKButton()}>OK</button>
            </div>
    </div>)

}