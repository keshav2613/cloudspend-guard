export interface DashboardResources {
  ec2: number
  ebs: number
  total: number
}

export interface DashboardFindings {
  total: number
  low_utilization_ec2: number
  unattached_ebs: number
}

export interface DashboardSummary {
  resources: DashboardResources
  findings: DashboardFindings
  estimated_monthly_savings_usd: number
}

export interface EC2Resource {
  instance_id: string
  instance_type: string
  state: string
  availability_zone: string
  private_ip: string | null
  public_ip: string | null
  name: string | null
}

export interface EBSResource {
  volume_id: string
  name: string | null
  volume_type: string
  size_gb: number
  state: string
  availability_zone: string
  encrypted: boolean
  attached: boolean
  attached_instance_ids: string[]
}

export interface DashboardResourcesData {
  ec2: EC2Resource[]
  ebs: EBSResource[]
}