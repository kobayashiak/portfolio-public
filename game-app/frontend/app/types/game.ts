
export interface Game{
    id:number;
    name:string;
    complete_rate:number;
    count?:number;
    is_owned:number
}

export interface GameDetail{
    game:Game;
    playtime:number;
    description:string;
    tags:Tag[];
    achievements:Achievement[];
    recommend_games:Game[];
}

export interface Tag{
    id:number;
    name:string;
    count:number;
}

export interface Achievement{
    id:number;
    api_name:string;
    display_name:string;
    percent:number;
    achieved:boolean;
    unlocktime:number;
    weight:number;
    description:string;
}

