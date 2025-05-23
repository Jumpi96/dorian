data "aws_route53_zone" "main" {
  name = "jplorenzo.com."
}

resource "aws_route53_record" "api" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "dorian-api.jplorenzo.com"
  type    = "A"

  alias {
    name                   = var.api_regional_domain_name
    zone_id                = var.api_zone_id
    evaluate_target_health = true
  }
} 