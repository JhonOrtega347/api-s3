import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    nombre_directorio = event['body']['directorio']
    
    # Proceso
    s3 = boto3.client('s3')
    # Crea un "objeto vacío" que simula un directorio
    key = f"{nombre_directorio.strip('/')}/"
    s3.put_object(Bucket=nombre_bucket, Key=key)
    
    # Salida
    return {
        'statusCode': 200,
        'mensaje': f'Directorio "{nombre_directorio}" creado exitosamente en el bucket "{nombre_bucket}".',
        'bucket': nombre_bucket,
        'directorio': key
    }
