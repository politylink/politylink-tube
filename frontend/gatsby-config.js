/**
 * @type {import('gatsby').GatsbyConfig}
 */
module.exports = {
    siteMetadata: {
        title: `politylink-video`,
        siteUrl: `https://www.yourdomain.tld`,
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
    ],
}
