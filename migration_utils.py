import streamlit as st

def collect_user_input(use_demo=False):
    # Nếu sử dụng demo, load demo data
    demo_data = None
    if use_demo:
        demo_data = create_demo_data()
    
    # Đặt selectbox này ngoài form để Streamlit rerun khi chọn
    migration_type = st.selectbox(
        "🔄 Kiểu migration",
        ["On-Premise ➜ Cloud", "Cloud ➜ Cloud"],
        index=1 if use_demo else 0,  # Chọn Cloud ➜ Cloud nếu demo
        help="Chọn kiểu migration: từ hệ thống tại chỗ lên Cloud, hoặc từ Cloud này sang Cloud khác. Sử dụng phím Tab để di chuyển giữa các trường.",
        key="migration_type_selectbox"
    )

    # Nếu là Cloud ➜ Cloud, chọn cloud_source ngoài form để dùng trong form
    cloud_source = None
    if migration_type == "Cloud ➜ Cloud":
        cloud_options = ["FCI Cloud", "AWS RDS", "Azure SQL", "Google Cloud SQL"]
        default_index = 1 if use_demo else 0  # AWS RDS cho demo
        cloud_source = st.selectbox(
            "🌩️ Cloud nguồn",
            cloud_options,
            index=default_index,
            help="Chọn Cloud nguồn nếu migration giữa các Cloud. Ví dụ: AWS RDS.",
            key="cloud_source_cloud2cloud"
        )

    with st.form("input_form"):
        if migration_type == "On-Premise ➜ Cloud":
            row1_col1, row1_col2, row1_col3 = st.columns([1, 1, 1])
            with row1_col1:
                db_type = st.selectbox(
                    "🔍 Loại Cơ sở dữ liệu",
                    ["PostgreSQL", "SQL Server", "MySQL", "MongoDB"],
                    help="Chọn loại CSDL bạn muốn migration. Ví dụ: PostgreSQL, SQL Server, MySQL, MongoDB.",
                    key=f"db_type_{migration_type}"
                )
            with row1_col2:
                version = st.text_input(
                    "🧾 Phiên bản",
                    "14",
                    help="Nhập phiên bản CSDL hiện tại. Ví dụ: 14 cho PostgreSQL.",
                    key=f"version_{migration_type}"
                )
            with row1_col3:
                data_size = st.text_input(
                    "💾 Dung lượng dữ liệu",
                    "1.2TB",
                    help="Tổng dung lượng dữ liệu cần migration. Ví dụ: 1.2TB.",
                    key=f"data_size_{migration_type}"
                )

            row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])
            with row2_col1:
                bandwidth = st.text_input(
                    "🌐 Băng thông mạng",
                    "5Gbps",
                    help="Băng thông mạng hiện có cho migration. Ví dụ: 5Gbps.",
                    key=f"bandwidth_{migration_type}"
                )
            with row2_col2:
                downtime = st.text_input(
                    "⏱ Downtime tối đa",
                    "10 phút",
                    help="Thời gian downtime tối đa cho phép. Ví dụ: 10 phút.",
                    key=f"downtime_{migration_type}"
                )
            with row2_col3:
                cloud_target = st.selectbox(
                    "☁️ Cloud đích",
                    ["FCI Cloud", "AWS RDS", "Azure SQL", "Google Cloud SQL"],
                    help="Chọn Cloud đích sau migration. Ví dụ: Google Cloud SQL.",
                    key=f"cloud_target_target_{migration_type}"
                )

            row3_col1, row3_col2, row3_col3 = st.columns([1, 1, 1])
            with row3_col1:
                security_level = st.selectbox(
                    "🔐 Mức độ bảo mật",
                    ["Chuẩn doanh nghiệp", "Tuân thủ PCI DSS", "Tuân thủ ISO 27001", "Cao nhất có thể"],
                    help="Chọn mức độ bảo mật yêu cầu. Ví dụ: Tuân thủ PCI DSS.",
                    key=f"security_{migration_type}"
                )
            with row3_col2:
                system_scale = st.selectbox(
                    "🏢 Quy mô hệ thống",
                    [ "Tập đoàn lớn", "Doanh nghiệp nhỏ", "Doanh nghiệp vừa", "Dữ liệu trọng yếu"],
                    help="Chọn quy mô hệ thống của bạn. Ví dụ: Doanh nghiệp nhỏ.",
                    key=f"system_scale_{migration_type}"
                )
            # row3_col3 để trống cho cân đối
            replication_type = None
            cloud_tool = None
            cloud_source_region = None
            cloud_target_region = None
            is_live_system = None
            ha_required = None
            vpc_configured = None
            rollback_strategy = None
        else:  # Cloud ➜ Cloud
            cloud_db_options = {
                "FCI Cloud": [
                    "IBM Db2",
                    "PostgreSQL (Managed by IBM)",
                    "Cloud SQL",
                    "Oracle on FCI"
                ],
                "AWS RDS": [
                    "Amazon Aurora",
                    "PostgreSQL",
                    "MySQL",
                    "SQL Server",
                    "MariaDB",
                    "Oracle"
                ],
                "Azure SQL": [
                    "Azure SQL Database",
                    "PostgreSQL (Azure)",
                    "MySQL (Azure)",
                    "SQL Server (Azure)"
                ],
                "Google Cloud SQL": [
                    "Cloud SQL for PostgreSQL",
                    "Cloud SQL for MySQL",
                    "Cloud SQL for SQL Server"
                ]
            }
            db_cloud_options = cloud_db_options.get(cloud_source, ["PostgreSQL", "MySQL", "SQL Server", "MongoDB"])

            row1_col1, row1_col2, row1_col3 = st.columns([1, 1, 1])
            with row1_col1:
                db_type = st.selectbox(
                    f"🔍 Loại Database của {cloud_source}",
                    db_cloud_options,
                    index=db_cloud_options.index(get_demo_value(demo_data, "db_type", "PostgreSQL")) if use_demo and get_demo_value(demo_data, "db_type", "PostgreSQL") in db_cloud_options else 0,
                    help=f"Chọn loại database phù hợp với {cloud_source}.",
                    key=f"db_type_{cloud_source}_{migration_type}"
                )
            with row1_col2:
                cloud_target_options = ["AWS", "FCI Cloud", "Azure", "Google Cloud"]
                cloud_target = st.selectbox(
                    "☁️ Cloud đích",
                    cloud_target_options,
                    index=cloud_target_options.index(get_demo_value(demo_data, "cloud_target", "Azure")) if use_demo and get_demo_value(demo_data, "cloud_target", "Azure") in cloud_target_options else 0,
                    help="Chọn Cloud đích sau migration. Ví dụ: Google Cloud SQL.",
                    key=f"cloud_target_source_{migration_type}"
                )
            with row1_col3:
                cloud_source_region = st.text_input(
                    "📍 Region nguồn",
                    get_demo_value(demo_data, "cloud_source_region", "Hồ Chí Minh"),
                    help="Nhập region của Cloud nguồn. Ví dụ: Hồ Chí Minh.",
                    key="cloud_source_region_input"
                )

            row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])
            with row2_col1:
                cloud_target_region = st.text_input(
                    "📍 Region đích",
                    get_demo_value(demo_data, "cloud_target_region", "Asia Pacific (Singapore)"),
                    help="Nhập region của Cloud đích. Ví dụ: Tokyo.",
                    key="cloud_target_region_input"
                )
            with row2_col2:
                replication_options = ["Full Snapshot", "CDC (Change Data Capture)"]
                replication_type = st.selectbox(
                    "🔁 Kiểu replication",
                    replication_options,
                    index=replication_options.index(get_demo_value(demo_data, "replication_type", "Full Snapshot")) if use_demo and get_demo_value(demo_data, "replication_type", "Full Snapshot") in replication_options else 0,
                    help="Chọn kiểu replication phù hợp. Full Snapshot hoặc CDC (Change Data Capture).",
                    key="replication_type_selectbox"
                )
            with row2_col3:
                cloud_tool_options = ["AWS DMS", "Azure Data Factory", "Google Database Migration Service", "Khác"]
                cloud_tool = st.selectbox(
                    "🛠 Công cụ sử dụng",
                    cloud_tool_options,
                    index=cloud_tool_options.index(get_demo_value(demo_data, "cloud_tool", "AWS DMS")) if use_demo and get_demo_value(demo_data, "cloud_tool", "AWS DMS") in cloud_tool_options else 0,
                    help="Chọn công cụ migration phù hợp với hệ thống của bạn.",
                    key="cloud_tool_selectbox"
                )

            row3_col1, row3_col2, row3_col3 = st.columns([1, 1, 1])
            with row3_col1:
                live_options = ["Có", "Không"]
                is_live_system = st.selectbox(
                    "🟢 Hệ thống đang chạy live?",
                    live_options,
                    index=0 if use_demo and get_demo_value(demo_data, "is_live_system") == "Có" else 1,
                    help="Hệ thống nguồn có đang chạy live không?",
                    key="is_live_system_selectbox"
                )
            with row3_col2:
                ha_options = ["Có", "Không"]
                ha_required = st.selectbox(
                    "🔁 Cần High Availability?",
                    ha_options,
                    index=0 if use_demo and get_demo_value(demo_data, "ha_required") == "Có" else 1,
                    help="Có yêu cầu High Availability (HA) không?",
                    key="ha_required_selectbox"
                )
            with row3_col3:
                vpc_options = ["Có", "Không"]
                vpc_configured = st.selectbox(
                    "🌐 Có cấu hình VPC/Subnet không?",
                    vpc_options,
                    index=0 if use_demo and get_demo_value(demo_data, "vpc_configured") == "Có" else 1,
                    help="Hệ thống đã cấu hình VPC/Subnet chưa?",
                    key="vpc_configured_selectbox"
                )

            row4_col1 = st.columns(1)[0]
            with row4_col1:
                rollback_strategy = st.text_area(
                    "🛡️ Kế hoạch rollback",
                    get_demo_value(demo_data, "rollback_strategy", "Tạo snapshot trước khi migration"),
                    help="Nhập kế hoạch rollback nếu migration thất bại. Ví dụ: Tạo snapshot trước khi migration.",
                    key="rollback_strategy_textarea"
                )

            row5_col1, row5_col2, row5_col3 = st.columns([1, 1, 1])
            with row5_col1:
                strategy_options = ["Lift & Shift", "Replatform", "Refactor"]
                migration_strategy = st.selectbox(
                    "📦 Chiến lược chuyển đổi",
                    strategy_options,
                    index=strategy_options.index(get_demo_value(demo_data, "migration_strategy", "Lift & Shift")) if use_demo and get_demo_value(demo_data, "migration_strategy", "Lift & Shift") in strategy_options else 0,
                    help="Chọn chiến lược migration: Lift & Shift (giữ nguyên), Replatform (thay đổi nền tảng), Refactor (viết lại).",
                    key="migration_strategy_selectbox"
                )
            with row5_col2:
                downtime_options = ["Không", "Có"]
                zero_downtime_required = st.selectbox(
                    "❗ Có yêu cầu Zero Downtime?",
                    downtime_options,
                    index=1 if use_demo and get_demo_value(demo_data, "zero_downtime_required") == "Có" else 0,
                    help="Hệ thống có yêu cầu chạy liên tục không downtime?",
                    key="zero_downtime_selectbox"
                )
            with row5_col3:
                testing_options = ["Có", "Không"]
                post_migration_testing = st.selectbox(
                    "🧪 Cần kiểm thử sau migration?",
                    testing_options,
                    index=0 if use_demo and get_demo_value(demo_data, "post_migration_testing") == "Có" else 1,
                    help="Có yêu cầu kiểm thử dữ liệu và hệ thống sau khi migration không?",
                    key="post_migration_testing_selectbox"
                )

            row6_col1, row6_col2, row6_col3 = st.columns([1, 1, 1])
            with row6_col1:
                dns_strategy = st.text_input(
                    "🌍 Chiến lược cập nhật DNS / Load Balancer",
                    get_demo_value(demo_data, "dns_strategy", "Sử dụng cut-over DNS sau kiểm thử"),
                    help="Ghi rõ cách định tuyến hệ thống mới sau migration. Ví dụ: chuyển DNS sau khi kiểm thử.",
                    key="dns_strategy_input"
                )
            with row6_col2:
                env_mapping = st.text_area(
                    "🔧 Biến môi trường cần chuyển đổi",
                    get_demo_value(demo_data, "env_mapping", "DB_HOST, API_ENDPOINT, ..."),
                    help="Liệt kê hoặc mô tả biến môi trường cần mapping khi chuyển hệ thống.",
                    key="env_mapping_input"
                )
            with row6_col3:
                monitoring_options = ["Có", "Không"]
                monitoring_required = st.selectbox(
                    "📈 Cần giám sát sau khi chuyển đổi?",
                    monitoring_options,
                    index=0 if use_demo and get_demo_value(demo_data, "monitoring_required") == "Có" else 1,
                    help="Có triển khai công cụ giám sát sau khi migration không?",
                    key="monitoring_required_selectbox"
                )

            # Thêm thông tin chi tiết cho Cloud-to-Cloud migration
            st.markdown("### 📊 Thông tin chi tiết dữ liệu")
            
            row7_col1, row7_col2, row7_col3 = st.columns([1, 1, 1])
            with row7_col1:
                data_size_gb = st.number_input(
                    "💾 Dung lượng dữ liệu (GB)",
                    min_value=1,
                    value=get_demo_value(demo_data, "data_size_gb", 100) if use_demo else 100,
                    help="Tổng dung lượng dữ liệu cần migration (GB)",
                    key="data_size_gb_input"
                )
            with row7_col2:
                data_type_options = ["Transactional", "Static Files", "Transactional + Static", "Real-time", "Batch"]
                data_type = st.selectbox(
                    "📋 Loại dữ liệu",
                    data_type_options,
                    index=data_type_options.index(get_demo_value(demo_data, "data_type", "Transactional")) if use_demo and get_demo_value(demo_data, "data_type", "Transactional") in data_type_options else 0,
                    help="Chọn loại dữ liệu chính trong hệ thống",
                    key="data_type_selectbox"
                )
            with row7_col3:
                change_rate_options = ["Thấp", "Trung bình", "Cao", "Rất cao"]
                change_rate = st.selectbox(
                    "🔄 Tốc độ thay đổi dữ liệu",
                    change_rate_options,
                    index=change_rate_options.index(get_demo_value(demo_data, "change_rate", "Trung bình")) if use_demo and get_demo_value(demo_data, "change_rate", "Trung bình") in change_rate_options else 1,
                    help="Tốc độ cập nhật/thêm/xóa dữ liệu hiện tại",
                    key="change_rate_selectbox"
                )

            row8_col1, row8_col2, row8_col3 = st.columns([1, 1, 1])
            with row8_col1:
                current_service = st.text_input(
                    "🏢 Dịch vụ hiện tại",
                    get_demo_value(demo_data, "current_service", "AWS RDS PostgreSQL"),
                    help="Dịch vụ cloud hiện tại (ví dụ: AWS RDS, Azure SQL, GCP Cloud SQL)",
                    key="current_service_input"
                )
            with row8_col2:
                target_service = st.text_input(
                    "🎯 Dịch vụ đích mong muốn",
                    get_demo_value(demo_data, "target_service", "Azure SQL Database"),
                    help="Dịch vụ cloud đích mong muốn",
                    key="target_service_input"
                )
            with row8_col3:
                network_options = ["Public Internet", "VPN", "Dedicated Interconnect", "Direct Connect/ExpressRoute"]
                network_connection = st.selectbox(
                    "🌐 Cách kết nối hiện tại",
                    network_options,
                    index=network_options.index(get_demo_value(demo_data, "network_connection", "VPN")) if use_demo and get_demo_value(demo_data, "network_connection", "VPN") in network_options else 1,
                    help="Phương thức kết nối giữa các cloud",
                    key="network_connection_selectbox"
                )

            row9_col1, row9_col2, row9_col3 = st.columns([1, 1, 1])
            with row9_col1:
                data_structure = st.text_area(
                    "🏗️ Cấu trúc dữ liệu",
                    get_demo_value(demo_data, "data_structure", "Schema, quan hệ, index, trigger, view, stored procedure..."),
                    help="Mô tả cấu trúc dữ liệu hiện tại",
                    key="data_structure_textarea"
                )
            with row9_col2:
                partitioning_options = ["Không có", "Có phân vùng", "Có sharding", "Phân mảnh cao"]
                data_partitioning = st.selectbox(
                    "📦 Phân vùng dữ liệu",
                    partitioning_options,
                    index=partitioning_options.index(get_demo_value(demo_data, "data_partitioning", "Không có")) if use_demo and get_demo_value(demo_data, "data_partitioning", "Không có") in partitioning_options else 0,
                    help="Tình trạng phân vùng/sharding dữ liệu",
                    key="data_partitioning_selectbox"
                )
            with row9_col3:
                downtime_tolerance = st.text_input(
                    "⏱️ Chấp nhận downtime",
                    get_demo_value(demo_data, "downtime_tolerance", "30 phút"),
                    help="Thời gian downtime tối đa có thể chấp nhận",
                    key="downtime_tolerance_input"
                )

            row10_col1, row10_col2 = st.columns([1, 1])
            with row10_col1:
                security_requirements = st.text_area(
                    "🔐 Yêu cầu bảo mật",
                    get_demo_value(demo_data, "security_requirements", "Mã hóa dữ liệu khi chuyển, IAM/ACLs, compliance..."),
                    help="Các yêu cầu bảo mật cần thiết",
                    key="security_requirements_textarea"
                )
            with row10_col2:
                compatibility_options = ["Không cần thay đổi", "Cần chỉnh sửa nhỏ", "Cần refactor lớn", "Cần viết lại"]
                app_compatibility = st.selectbox(
                    "🔧 Độ tương thích ứng dụng",
                    compatibility_options,
                    index=compatibility_options.index(get_demo_value(demo_data, "app_compatibility", "Không cần thay đổi")) if use_demo and get_demo_value(demo_data, "app_compatibility", "Không cần thay đổi") in compatibility_options else 0,
                    help="Mức độ cần chỉnh sửa ứng dụng",
                    key="app_compatibility_selectbox"
                )

            row11_col1 = st.columns(1)[0]
            with row11_col1:
                external_dependencies = st.text_area(
                    "🔗 Dịch vụ tích hợp bên ngoài",
                    get_demo_value(demo_data, "external_dependencies", "Salesforce API, RabbitMQ, Redis, Elasticsearch..."),
                    help="Các dịch vụ bên ngoài hệ thống cần chuyển cấu hình",
                    key="external_dependencies_textarea"
                )
            version = None
            data_size = None
            bandwidth = None
            downtime = None
            security_level = None
            system_scale = None

        submit = st.form_submit_button("🚀 Tạo kế hoạch Migration")

    # Phản hồi sau khi submit
    if 'submit' in locals() and submit:
        st.success("✅ Đã nhận thông tin. Đang xử lý kế hoạch migration...")

    result = {
        "submit": submit,
        "migration_type": migration_type,
        "db_type": db_type,
        "version": version,
        "data_size": data_size,
        "bandwidth": bandwidth,
        "downtime": downtime,
        "cloud_target": cloud_target,
        "cloud_source": cloud_source if migration_type == "Cloud ➜ Cloud" else "On-Premise",
        "security_level": security_level,
        "system_scale": system_scale,
    }
    # Add extra fields for Cloud ➜ Cloud
    if migration_type == "Cloud ➜ Cloud":
        result.update({
            "replication_type": replication_type,
            "cloud_tool": cloud_tool,
            "cloud_source_region": cloud_source_region,
            "cloud_target_region": cloud_target_region,
            "is_live_system": is_live_system,
            "ha_required": ha_required,
            "vpc_configured": vpc_configured,
            "rollback_strategy": rollback_strategy,
            "migration_strategy": migration_strategy,
            "zero_downtime_required": zero_downtime_required,
            "post_migration_testing": post_migration_testing,
            "dns_strategy": dns_strategy,
            "env_mapping": env_mapping,
            "monitoring_required": monitoring_required,
            # Thông tin chi tiết dữ liệu
            "data_size_gb": data_size_gb,
            "data_type": data_type,
            "change_rate": change_rate,
            "current_service": current_service,
            "target_service": target_service,
            "network_connection": network_connection,
            "data_structure": data_structure,
            "data_partitioning": data_partitioning,
            "downtime_tolerance": downtime_tolerance,
            "security_requirements": security_requirements,
            "app_compatibility": app_compatibility,
            "external_dependencies": external_dependencies,
        })
    return result

def build_system_info(user_input):
    system_info = f"""
- Kiểu Migration: {user_input['migration_type']}
- Cloud nguồn: {user_input['cloud_source']}
- Cloud đích: {user_input['cloud_target']}
- Database: {user_input['db_type']}, phiên bản {user_input['version']}
- Dung lượng dữ liệu: {user_input['data_size']}
- Băng thông mạng: {user_input['bandwidth']}
- Downtime tối đa: {user_input['downtime']}
- Mức độ bảo mật: {user_input['security_level']}
- Quy mô hệ thống: {user_input['system_scale']}
"""
    if user_input.get("migration_type") == "Cloud ➜ Cloud":
        system_info += f"""
- Công cụ: {user_input.get('cloud_tool','')}
- Kiểu replication: {user_input.get('replication_type','')}
- Cloud source region: {user_input.get('cloud_source_region','')}
- Cloud target region: {user_input.get('cloud_target_region','')}
- Live system: {user_input.get('is_live_system','')}
- HA Required: {user_input.get('ha_required','')}
- VPC/Subnet Configured: {user_input.get('vpc_configured','')}
- Rollback Strategy: {user_input.get('rollback_strategy','')}
- Chiến lược migration: {user_input.get('migration_strategy','')}
- Zero Downtime yêu cầu: {user_input.get('zero_downtime_required','')}
- Kiểm thử sau migration: {user_input.get('post_migration_testing','')}
- DNS / Load Balancer Strategy: {user_input.get('dns_strategy','')}
- Biến môi trường cần mapping: {user_input.get('env_mapping','')}
- Giám sát sau migration: {user_input.get('monitoring_required','')}

📊 THÔNG TIN CHI TIẾT DỮ LIỆU:
- Dung lượng dữ liệu: {user_input.get('data_size_gb','')} GB
- Loại dữ liệu: {user_input.get('data_type','')}
- Tốc độ thay đổi: {user_input.get('change_rate','')}
- Dịch vụ hiện tại: {user_input.get('current_service','')}
- Dịch vụ đích: {user_input.get('target_service','')}
- Kết nối mạng: {user_input.get('network_connection','')}
- Cấu trúc dữ liệu: {user_input.get('data_structure','')}
- Phân vùng dữ liệu: {user_input.get('data_partitioning','')}
- Chấp nhận downtime: {user_input.get('downtime_tolerance','')}
- Yêu cầu bảo mật: {user_input.get('security_requirements','')}
- Tương thích ứng dụng: {user_input.get('app_compatibility','')}
- Dịch vụ tích hợp: {user_input.get('external_dependencies','')}
"""
    return system_info

def build_json_for_ai(user_input):
    """
    Tạo định dạng JSON chuẩn hóa cho AI xử lý migration
    """
    import json
    
    # Xử lý downtime tolerance từ text sang minutes
    downtime_text = user_input.get('downtime_tolerance', '30 phút')
    downtime_minutes = 30  # default
    if 'phút' in downtime_text or 'minute' in downtime_text:
        try:
            downtime_minutes = int(''.join(filter(str.isdigit, downtime_text)))
        except:
            downtime_minutes = 30
    
    # Xử lý data partitioning từ text sang boolean
    partitioning_text = user_input.get('data_partitioning', 'Không có')
    data_partitioning = partitioning_text not in ['Không có', 'None']
    
    # Xử lý change rate mapping
    change_rate_mapping = {
        'Thấp': 'Low',
        'Trung bình': 'Medium', 
        'Cao': 'High',
        'Rất cao': 'Very High'
    }
    data_change_rate = change_rate_mapping.get(user_input.get('change_rate', 'Trung bình'), 'Medium')
    
    # Xử lý network type mapping
    network_mapping = {
        'Public Internet': 'Public',
        'VPN': 'VPN',
        'Dedicated Interconnect': 'Dedicated',
        'Direct Connect/ExpressRoute': 'DirectConnect'
    }
    network_type = network_mapping.get(user_input.get('network_connection', 'VPN'), 'VPN')
    
    # Xử lý external dependencies từ text sang list
    external_deps_text = user_input.get('external_dependencies', '')
    external_integrations = []
    if external_deps_text:
        # Tách các dịch vụ bằng dấu phẩy hoặc xuống dòng
        deps = external_deps_text.replace('\n', ',').split(',')
        external_integrations = [dep.strip() for dep in deps if dep.strip()]
    
    # Xử lý security requirements
    security_text = user_input.get('security_requirements', '')
    security_policies = []
    if 'mã hóa' in security_text.lower() or 'encryption' in security_text.lower():
        security_policies.append('AES256 encryption')
    if 'iam' in security_text.lower():
        security_policies.append('Preserve IAM')
    if 'compliance' in security_text.lower():
        security_policies.append('Compliance requirements')
    if not security_policies:
        security_policies = ['Standard encryption']
    
    # Xác định critical level dựa trên các yếu tố
    critical_level = 'Medium'
    if (user_input.get('zero_downtime_required') == 'Có' or 
        user_input.get('ha_required') == 'Có' or
        user_input.get('data_size_gb', 0) > 500):
        critical_level = 'High'
    elif user_input.get('data_size_gb', 0) < 50:
        critical_level = 'Low'
    
    # Tạo JSON structure
    migration_json = {
        "current_cloud_provider": user_input.get('cloud_source', 'Unknown'),
        "target_cloud_provider": user_input.get('cloud_target', 'Unknown'),
        "data_type": user_input.get('data_type', 'Transactional'),
        "data_size_gb": user_input.get('data_size_gb', 100),
        "data_change_rate": data_change_rate,
        "downtime_window_minutes": downtime_minutes,
        "network_type": network_type,
        "data_partitioning": data_partitioning,
        "source_services": [user_input.get('current_service', 'Unknown')],
        "target_services": [user_input.get('target_service', 'Unknown')],
        "security_policies": security_policies,
        "external_integrations": external_integrations,
        "app_dependency_notes": user_input.get('app_compatibility', 'No changes required'),
        "schema_notes": user_input.get('data_structure', 'Standard schema'),
        "critical_level": critical_level,
        # Thêm các trường bổ sung
        "migration_strategy": user_input.get('migration_strategy', 'Lift & Shift'),
        "zero_downtime_required": user_input.get('zero_downtime_required') == 'Có',
        "post_migration_testing": user_input.get('post_migration_testing') == 'Có',
        "monitoring_required": user_input.get('monitoring_required') == 'Có',
        "replication_type": user_input.get('replication_type', 'Full Snapshot'),
        "cloud_tool": user_input.get('cloud_tool', 'AWS DMS'),
        "source_region": user_input.get('cloud_source_region', 'Unknown'),
        "target_region": user_input.get('cloud_target_region', 'Unknown'),
        "is_live_system": user_input.get('is_live_system') == 'Có',
        "ha_required": user_input.get('ha_required') == 'Có',
        "vpc_configured": user_input.get('vpc_configured') == 'Có',
        "rollback_strategy": user_input.get('rollback_strategy', 'Create snapshot before migration'),
        "dns_strategy": user_input.get('dns_strategy', 'Cut-over DNS after testing'),
        "env_mapping": user_input.get('env_mapping', 'DB_HOST, API_ENDPOINT'),
        "migration_type": user_input.get('migration_type', 'Cloud ➜ Cloud')
    }
    
    return json.dumps(migration_json, indent=2, ensure_ascii=False)

def get_demo_value(demo_data, key, default=""):
    """
    Lấy giá trị demo cho input field
    """
    if demo_data and key in demo_data:
        return demo_data[key]
    return default

def create_demo_data():
    """
    Tạo dữ liệu demo cho Cloud-to-Cloud migration
    """
    demo_data = {
        "migration_type": "Cloud ➜ Cloud",
        "cloud_source": "AWS",
        "cloud_target": "Azure",
        "db_type": "PostgreSQL",
        "version": "14",
        "data_size": "850 GB",
        "bandwidth": "1 Gbps",
        "downtime": "30 phút",
        "cloud_target": "Azure",
        "cloud_source": "AWS",
        "security_level": "Tuân thủ PCI DSS",
        "system_scale": "Tập đoàn lớn",
        "replication_type": "CDC (Change Data Capture)",
        "cloud_tool": "AWS DMS",
        "cloud_source_region": "US East (N. Virginia)",
        "cloud_target_region": "East US",
        "is_live_system": "Có",
        "ha_required": "Có",
        "vpc_configured": "Có",
        "rollback_strategy": "Tạo snapshot trước khi migration, backup real-time",
        "migration_strategy": "Replatform",
        "zero_downtime_required": "Có",
        "post_migration_testing": "Có",
        "dns_strategy": "Blue-green deployment với cut-over DNS",
        "env_mapping": "DB_HOST, API_ENDPOINT, S3_BUCKET, LAMBDA_FUNCTIONS",
        "monitoring_required": "Có",
        # Thông tin chi tiết dữ liệu
        "data_size_gb": 850,
        "data_type": "Transactional + Static",
        "change_rate": "Trung bình",
        "current_service": "AWS S3, RDS PostgreSQL, Lambda",
        "target_service": "Azure Blob Storage, Azure Database for PostgreSQL, Azure Functions",
        "network_connection": "VPN",
        "data_structure": "Schema phức tạp với stored procedures, triggers, views. Phân vùng theo khu vực và khách hàng. Index tối ưu cho queries thường xuyên.",
        "data_partitioning": "Có phân vùng",
        "downtime_tolerance": "30 phút",
        "security_requirements": "Mã hóa AES256 khi chuyển dữ liệu, giữ nguyên phân quyền IAM, tuân thủ PCI DSS, audit trail đầy đủ",
        "app_compatibility": "Cần chỉnh sửa nhỏ",
        "external_dependencies": "Salesforce API, RabbitMQ, Redis Cache, Elasticsearch, Payment Gateway"
    }
    return demo_data

def display_migration_json(user_input):
    """
    Hiển thị JSON format cho AI trong Streamlit
    """
    import streamlit as st
    
    json_data = build_json_for_ai(user_input)
    
    st.markdown("### 🤖 Dữ liệu JSON cho AI xử lý")
    st.code(json_data, language="json")
    
    # Thêm nút copy
    st.markdown("**📋 Click để copy JSON data:**")
    st.text_area("JSON Data", json_data, height=300, key="json_display")
    
    return json_data

def build_ai_prompt_with_json(user_input):
    """
    Tạo prompt cho AI với JSON format
    """
    json_data = build_json_for_ai(user_input)
    
    prompt = f"""
Bạn là chuyên gia Cloud Migration với 15+ năm kinh nghiệm. 
Dưới đây là thông tin chi tiết về dự án migration:

```json
{json_data}
```

Dựa trên thông tin này, hãy tạo một kế hoạch migration chi tiết bao gồm:

1. **Phân tích rủi ro và thách thức**
2. **Chiến lược migration phù hợp** (dựa trên data_change_rate, downtime_window_minutes)
3. **Timeline chi tiết** (dựa trên data_size_gb, network_type)
4. **Công cụ và script cần thiết**
5. **Kế hoạch rollback**
6. **Checklist validation**
7. **Ước tính chi phí** (nếu có thể)

Hãy đưa ra các khuyến nghị cụ thể dựa trên:
- Critical level: {user_input.get('critical_level', 'Medium')}
- Network type: {user_input.get('network_connection', 'VPN')}
- Data partitioning: {user_input.get('data_partitioning', 'Không có')}
- External integrations: {user_input.get('external_dependencies', 'None')}
"""
    
    return prompt

def show_demo_migration():
    """
    Hiển thị demo migration với dữ liệu mẫu
    """
    import streamlit as st
    
    demo_data = create_demo_data()
    
    st.markdown("## 🚀 Demo: Cloud-to-Cloud Migration")
    st.markdown("### 📊 Thông tin nền tảng & dịch vụ")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Nền tảng hiện tại:** AWS")
        st.markdown("**Nền tảng đích:** Azure")
        st.markdown("**Loại dữ liệu:** Transactional + Static")
        st.markdown("**Dung lượng dữ liệu:** ~850 GB")
        st.markdown("**Tốc độ thay đổi dữ liệu:** Trung bình (1–5% mỗi giờ)")
        st.markdown("**Cửa sổ downtime cho phép:** 30 phút")
        st.markdown("**Mạng truyền dữ liệu:** VPN riêng")
    
    with col2:
        st.markdown("**Phân vùng dữ liệu:** Có (theo khu vực, khách hàng)")
        st.markdown("**Dịch vụ nguồn:** S3, RDS (PostgreSQL), Lambda")
        st.markdown("**Dịch vụ đích tương ứng:** Blob Storage, Azure Database, Azure Functions")
        st.markdown("**Chính sách bảo mật:** Mã hóa AES256, giữ nguyên phân quyền IAM")
        st.markdown("**Tích hợp hệ thống ngoài:** Salesforce API, RabbitMQ")
        st.markdown("**Phụ thuộc ứng dụng:** Cần cập nhật connection string sau migration")
        st.markdown("**Mức độ quan trọng:** Cao (ảnh hưởng trực tiếp đến kinh doanh)")
    
    st.markdown("### 🤖 JSON Output cho AI xử lý")
    
    # Tạo JSON từ demo data
    json_output = build_json_for_ai(demo_data)
    
    st.code(json_output, language="json")
    
    st.markdown("### 📋 Thông tin chi tiết được xử lý:")
    
    # Hiển thị system info
    system_info = build_system_info(demo_data)
    st.text(system_info)
    
    return demo_data, json_output

def build_prompts(system_info, migration_type=None):
    # Nếu migration_type chưa truyền vào, lấy từ system_info nếu có
    if migration_type is None and isinstance(system_info, dict):
        migration_type = system_info.get('migration_type', None)
    elif migration_type is None and isinstance(system_info, str):
        migration_type = None

    # Prompt cho Cloud ➜ Cloud sẽ nhấn mạnh phân tích sự khác biệt giữa các cloud
    overview_prompt = f"""
Bạn là chuyên gia về migration cơ sở dữ liệu với 20 năm kinh nghiệm. Với thông tin sau:
{system_info}

👉 Hãy phân tích tổng quan hệ thống và giải thích vì sao nên chọn chiến lược phù hợp (Logical Replication vs Snapshot vs Dump & Restore).
"""
    if migration_type == "Cloud ➜ Cloud":
        overview_prompt += "\nNếu migration là từ Cloud ➜ Cloud, hãy phân tích thêm sự khác biệt giữa các nền tảng cloud, tương thích công cụ và chi phí."

    return {
        "overview": overview_prompt,
        "steps": f"""
Bạn là chuyên gia triển khai migration hệ thống phức tạp. Với thông tin:
{system_info}

👉 Hãy mô tả chi tiết các bước migration theo 3 giai đoạn: Before, During, After. Bao gồm:
- Checklist kỹ thuật
- Chiến lược rollback nếu lỗi
- Gợi ý công cụ (pg_dump, Bucardo, DMS, v.v.)
- Ghi chú đơn giản cho người mới
""",
        "time_estimation": f"""
Bạn là kỹ sư mạng. Với dữ liệu dung lượng {system_info}, hãy tính toán thời gian truyền tải chi tiết (đổi đơn vị nếu cần), bao gồm margin thời gian cho downtime, kiểm thử và xử lý bất ngờ.
""",
        "security": f"""
Bạn là chuyên gia bảo mật. Với yêu cầu hệ thống:
{system_info}

👉 Hãy đề xuất chiến lược bảo mật toàn diện cho migration, bao gồm:
- IAM, mã hóa dữ liệu
- Logging & Audit trail
- Công cụ cloud-native khuyến nghị
""",
        "validation": f"""
Sau migration, làm sao để đảm bảo dữ liệu đúng và hệ thống hoạt động chuẩn?
👉 Viết checklist xác minh dữ liệu: checksum, query test, hiệu năng, so sánh kết quả.
""",
        "improvement": f"""
Sau migration, hệ thống có thể cải tiến ra sao?
👉 Đề xuất: High Availability, Hybrid Cloud, tự động hóa DevOps...
""",
        "cloud_architect_plan": f"""
Bạn hãy đóng vai trò là một chuyên gia Cloud Architect.
Tôi muốn bạn giúp thiết kế một kế hoạch migration hệ thống từ [nguồn] sang [đích].
Với thông tin sau:
{system_info}

Hãy trình bày kế hoạch theo cấu trúc dễ hiểu gồm các phần sau:
1. Tổng quan ngắn gọn về mục tiêu migration
2. Các bước chi tiết, đánh số rõ ràng (1, 2, 3...)
3. Thời gian dự kiến cho từng bước
4. Băng thông cần thiết và dung lượng truyền tải (ước lượng theo GB và Mbps nếu có thể)
5. Sơ đồ kiến trúc trước và sau khi migration (có thể mô tả bằng sơ đồ text hoặc biểu đồ block đơn giản)
6. Các rủi ro và cách giảm thiểu
7. Gợi ý công cụ hoặc script hỗ trợ (nếu có)
""",
        "ai_json_analysis": build_ai_prompt_with_json(system_info) if isinstance(system_info, dict) else f"""
Bạn là chuyên gia Cloud Migration với 15+ năm kinh nghiệm. 
Với thông tin sau:
{system_info}

Hãy tạo một kế hoạch migration chi tiết bao gồm:
1. **Phân tích rủi ro và thách thức**
2. **Chiến lược migration phù hợp**
3. **Timeline chi tiết**
4. **Công cụ và script cần thiết**
5. **Kế hoạch rollback**
6. **Checklist validation**
7. **Ước tính chi phí** (nếu có thể)
"""
    } 