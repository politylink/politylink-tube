require("dotenv").config({
    path: `.env`,
})

/**
 * @type {import('gatsby').GatsbyConfig}
 */
module.exports = {
    siteMetadata: {
        title: `PolityLink｜国会を、もっとおもしろく。`,
        description: `PolityLink（ポリティリンク）は、国会がもっとおもしろくなる動画サイトです。国会中継を文字起こしと一緒に再生することで、いま国会でどんなことが話題なのか簡単にチェックできます。`,
        twitterUsername: `@politylink`,
        twitterCard: `summary`,
        siteUrl: `https://politylink.jp`,
        imageUrl: `https://politylink.jp/logo.png`
    },
    plugins: [
        `gatsby-transformer-json`,
        {
            resolve: `gatsby-source-filesystem`,
            options: {
                path: `${__dirname}/artifact/clip`,
            },
        },
        {
            resolve: `gatsby-plugin-s3`,
            options: {
                bucketName: "politylink-gatsby",
                protocol: "https",
                hostname: "politylink.jp",
            },
        },
        {
            resolve: `gatsby-plugin-google-gtag`,
            options: {
                trackingIds: [process.env.GOOGLE_ANALYTICS_TRACKING_ID],
            },
        },
        {
            resolve: `gatsby-plugin-manifest`,
            options: {
                name: `PolityLink`,
                short_name: `PolityLink`,
                start_url: `/`,
                background_color: `#174a5c`,
                theme_color: `#174a5c`,
                icon: `static/logo.png`,
            },
        },
        {
            resolve: `gatsby-source-filesystem`,
            options: {
                name: `markdowns`,
                path: `${__dirname}/src/markdowns/`,
            },
        },
        `gatsby-transformer-remark`,
    ],
}
