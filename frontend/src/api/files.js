const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Subir un archivo (puede ser firmado o no)
export async function uploadFile(file, signed = false) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('signed', signed)

    const response = await fetch(`${API_BASE_URL}/files/upload`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('jwt_token')}`,
        },
        body: formData,
    })

    if (!response.ok) {
        const err = await response.text()
        throw new Error(err || 'Upload failed')
    }

    return await response.json()
}

// Descargar un archivo
export async function downloadFile(fileId) {
    const response = await fetch(`${API_BASE_URL}/files/${fileId}/download`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('jwt_token')}`,
        },
    })

    if (!response.ok) {
        const err = await response.text()
        throw new Error(err || 'Download failed')
    }

    const blob = await response.blob()
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = fileId
    link.click()
}

// Validar la firma de un archivo
export async function validateFileSignature(fileId) {
    const response = await fetch(`${API_BASE_URL}/files/${fileId}/validate-signature`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('jwt_token')}`,
        },
    })

    if (!response.ok) {
        const err = await response.text()
        throw new Error(err || 'Signature validation failed')
    }

    return await response.json()
}


