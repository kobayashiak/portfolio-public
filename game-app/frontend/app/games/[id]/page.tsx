import { GameDetailComponent } from "@/app/components/GameDetail"
import {fetchDetail} from '../../lib/api'


export async function generateMetadata({params}:{params:Promise<{id:string}>}){
  const {id} = await params;
  const name = (await fetchDetail(id)).game.name;
  return{
    title:`${name}の詳細情報| Steam Game Manager`,
    description: `${name}のクリア率や実績などの詳細データを確認できます。`
  }

}



export default async function GameDetailPage({params}:{params:Promise<{id:string}>}){
    const {id} = await params
            try{
                    const gameDetail = await fetchDetail(id);
                    return(<div><GameDetailComponent gameDetail = {gameDetail} id = {id}/></div>)
                }catch(err){
                    console.log(`エラー発生：${err}`)   
                }
}