import boto3
import base64

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    nombre_directorio = event['body']['directorio']
    nombre_archivo = event['body']['archivo']
    contenido_base64 = event['body']['contenido']
    
    # Proceso
    s3 = boto3.client('s3')
    
    # Convertir el contenido de base64 a bytes
    contenido_bytes = base64.b64decode(contenido_base64)
    
    # Definir la ruta (directorio + nombre del archivo)
    key = f"{nombre_directorio.strip('/')}/{nombre_archivo}"
    
    # Subir el archivo
    s3.put_object(
        Bucket=nombre_bucket,
        Key=key,
        Body=contenido_bytes
    )
    
    # Salida
    return {
        'statusCode': 200,
        'mensaje': f'Archivo "{nombre_archivo}" subido exitosamente al directorio "{nombre_directorio}" del bucket "{nombre_bucket}".',
        'bucket': nombre_bucket,
        'directorio': nombre_directorio,
        'archivo': nombre_archivo
    }
