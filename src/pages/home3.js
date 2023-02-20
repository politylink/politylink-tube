import * as React from "react"
import HomeLayout from "../layout/homeLayout";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import VideoCard from "../components/videoCard";


const HomePage3 = () => {
    return (
        <HomeLayout value={2}>
            <Container maxWidth="lg" sx={{padding: 0}}>
                <Grid container spacing={1}>
                    <VideoCard
                        imageUrl="https://image.politylink.jp/clips/clip/l/100.jpg"
                        title="高圧ガス保安法の法令違反件数に係る審議会資料等の誤りが発生した原因"
                        date="2023年2月10日"
                        duration="0h20m"
                        place="衆議院 予算委員会"
                        speaker="田中太郎"
                    />
                    <VideoCard
                        imageUrl="https://image.politylink.jp/clips/clip/l/1000.jpg"
                        title="子供が社会に出るに当たって身に付けるべき知識を学校で積極的に教えていく必要性"
                        date="2023年2月10日"
                        duration="0h4m"
                        place="衆議院 予算委員会"
                        speaker="田中太郎"
                    />
                    <VideoCard
                        imageUrl="https://image.politylink.jp/clips/clip/l/1000.jpg"
                        title="新型コロナウイルス感染症対策における中小企業支援策の評価と今後の方針"
                        date="2023年2月10日"
                        duration="0h12m"
                        place="参議院 北朝鮮による拉致問題等に関する特別委員会"
                        speaker="田中太郎"
                    />
                    <VideoCard
                        imageUrl="https://image.politylink.jp/clips/clip/l/100.jpg"
                        title="高圧ガス保安法の法令違反件数に係る審議会資料等の誤りが発生した原因"
                        date="2023年2月10日"
                        duration="0h20m"
                        place="衆議院 予算委員会"
                        speaker="田中太郎"
                    />
                    <VideoCard
                        imageUrl="https://image.politylink.jp/clips/clip/l/1000.jpg"
                        title="子供が社会に出るに当たって身に付けるべき知識を学校で積極的に教えていく必要性"
                        date="2023年2月10日"
                        duration="0h4m"
                        place="衆議院 予算委員会"
                        speaker="田中太郎"
                    />
                    <VideoCard
                        imageUrl="https://image.politylink.jp/clips/clip/l/1000.jpg"
                        title="新型コロナウイルス感染症対策における中小企業支援策の評価と今後の方針"
                        date="2023年2月10日"
                        duration="0h12m"
                        place="参議院 北朝鮮による拉致問題等に関する特別委員会"
                        speaker="田中太郎"
                    />
                </Grid>
            </Container>
        </HomeLayout>
    )
}

export default HomePage3;