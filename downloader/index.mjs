import { Octokit } from 'octokit'
import { spawnSync } from 'child_process'
import { readFileSync, rmSync, statSync } from 'fs'

const DOWNLOAD = false
const token = loadToken()
const gh = new Octokit({ auth: token })

function loadToken() {
  try {
    return readFileSync('.env', 'utf8')
  } catch {
    return null
  }
}

/** @returns {string} */
function buildCurl(asset, token) {
  let cmd = `curl -o ${asset.name} -L -H "Accept: application/octet-stream"`
  if (token) cmd += ` -H "Authorization: Bearer ${token}"`
  return cmd + ` https://api.github.com/repos/nguyenvukhang/backblaze/releases/assets/${asset.id}`
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

    let exists = false
    let downloaded = false
    console.log(asset.id)
    try {
      downloaded = statSync(asset.name).size === asset.size
      exists = true
    } catch {}

    if (DOWNLOAD && !downloaded) {
      rmSync(asset.name, { force: true })
      console.log('[download]', asset.name, '...')
      spawnSync(buildCurl(asset, token), { stdio: 'inherit', shell: true })
    } else {
      console.log('[skip]', asset.name)
    }
  }
}

main().finally(() => process.exit())
