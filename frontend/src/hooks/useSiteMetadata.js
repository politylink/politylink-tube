import {graphql, useStaticQuery} from "gatsby"

export const useSiteMetadata = () => {
    const data = useStaticQuery(graphql`
    query {
      site {
        siteMetadata {
          title
          description
          twitterUsername
          twitterCard
          siteUrl
          imageUrl
        }
      }
    }
  `)
    return data.site.siteMetadata
}