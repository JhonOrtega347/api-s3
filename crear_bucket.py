import boto3
import json
import re

def lambda_handler(event, context):
    # --- Entrada ---
    body = event.get('body', {})

    # Si el body llega como string (API Gateway suele enviarlo así)
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Body no es un JSON válido"})
            }

    nombre_bucket = body.get('bucket', '').strip()

    # --- Validación del nombre del bucket ---
    if not nombre_bucket:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Falta el nombre del bucket"})
        }

    # Regex para validar reglas de S3
    patron = r'^[a-z0-9]([a-z0-9\-]{1,61}[a-z0-9])?$'
    if not re.match(patron, nombre_bucket):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Nombre de bucket inválido. Solo minúsculas, números y guiones; 3-63 caracteres."})
        }

    # --- Proceso ---
    s3 = boto3.client('s3')
    region = boto3.session.Session().region_name

    try:
        if region == 'us-east-1':
            response = s3.create_bucket(Bucket=nombre_bucket)
        else:
            response = s3.create_bucket(
                Bucket=nombre_bucket,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
    except s3.exceptions.BucketAlreadyExists:
        return {
            "statusCode": 409,
            "body": json.dumps({"error": f'El bucket "{nombre_bucket}" ya existe en AWS.'})
        }
    except s3.exceptions.ClientError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    # --- Salida ---
    return {
        "statusCode": 200,
        "body": json.dumps({
            "mensaje": f'Bucket "{nombre_bucket}" creado exitosamente en la región "{region}".',
            "location": response.get('Location', region)
        })
    }
