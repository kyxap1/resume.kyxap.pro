# filters/merge.jq
# Usage: jq -s -f filters/merge.jq --arg role "devops" companies/*.json skills/_common.json skills/devops.json

# The input is a stream of JSON objects (companies and skills).
# We need to separate them and construct the final object.

# 1. Collect all inputs into an array
# 1. Separate base (resume.json), override (specialties/*.json), and other inputs
.[0] as $base |
.[1] as $override |
.[2:] as $others |

# 2. Construct the final object
($base * $override) + {
  work: (
    $others
    | map(select(type == "object" and has("company") and (.hidden | not)))
    | sort_by(.startDate)
    | reverse
    | map(
        (.descriptions[$role] // .descriptions["devops"]) as $desc |
        {
        company: .company,
        website: .website,
        startDate: .startDate,
        endDate: .endDate,
        position: $desc.position,
        business: $desc.business,
        address: $desc.address,
        summary: $desc.summary,
        highlights: $desc.highlights,
        projects: $desc.projects
      })
  ),
  skills: (
    $others
    | map(select(type == "object" and has("skills")))
    | map(.skills)
    | flatten
  )
}
