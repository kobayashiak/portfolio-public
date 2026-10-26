import {url} from '../url'
import { GameDetail } from '../types/game';


export const fetchDetail = async (id:string):Promise<GameDetail>=>{
                    const response = await fetch(`${url}/gameDetail/${id}`);
                    if (!response.ok) throw new Error(`ゲーム詳細情報の取得に失敗しました。:${response.status}`)
                    return response.json();
        }