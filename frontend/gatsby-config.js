require("dotenv").config({
    path: `.env`,
})

/**
 * @type {import('gatsby').GatsbyConfig}
 */
module.exports = {
    siteMetadata: {
        title: `PolityLink｜国会を、もっとおもしろく。`,
        description: `PolityLink（ポリティリンク）は、国会をあなたの身近なものへと変える動画サイトです。国会中継がクリップ（短編動画）として切り出され、トピックごとに整理されているため、注目の話題や、気になる議題を簡単にチェックできます。`,
        twitterUsername: `@politylink`,
        twitterCard: `summary`,
        siteUrl: `https://politylink.jp`,
        imageUrl: `https://image.politylink.jp/clips/summary.jpg`
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
