import { Octokit } from 'octokit'
import { readFileSync, statSync } from 'fs'

const token = loadToken()
const gh = new Octokit({ auth: token })

function loadToken() {
  try {
    return readFileSync('.env', 'utf8')
  } catch {
    return null
  }
}

async function main() {
  const rel = await gh.rest.repos.getReleaseByTag({
    owner: 'nguyenvukhang',
    repo: 'backblaze',
    tag: 'v0.2',
  })
  console.log('Found', rel.data.assets.length, 'assets')
  for (let i = 0; i < rel.data.assets.length; i++) {
    const asset = rel.data.assets[i]

    let stat
    try {
      stat = statSync(asset.name)
    } catch {
      console.log('Error while attemtping stat', asset.name)
      continue
    }

    if (stat.size === asset.size) {
      console.log('Ok!', asset.name)
    } else {
      console.log('!!!', asset.name, `(${stat.size}/${asset.size})`)
    }
  }
}

main().finally(() => process.exit())
