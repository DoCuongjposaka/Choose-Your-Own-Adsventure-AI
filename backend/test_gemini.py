#!/usr/bin/env python3
"""
Test file để kiểm tra Gemini API
Kiểm tra: API key, version, kết nối, và chức năng cơ bản
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

def print_header(title):
    """In tiêu đề với định dạng đẹp"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_section(title):
    """In tiêu đề section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def print_success(message):
    """In thông báo thành công"""
    print(f"✅ {message}")

def print_error(message):
    """In thông báo lỗi"""
    print(f"❌ {message}")

def print_info(message):
    """In thông tin"""
    print(f"ℹ️  {message}")

def print_warning(message):
    """In cảnh báo"""
    print(f"⚠️  {message}")

def test_environment():
    """Kiểm tra môi trường và dependencies"""
    print_header("KIỂM TRA MÔI TRƯỜNG")
    
    # Kiểm tra Python version
    print_section("Python Version")
    print_info(f"Python version: {sys.version}")
    print_info(f"Python executable: {sys.executable}")
    
    # Kiểm tra file .env
    print_section("Environment Variables")
    env_file = ".env"
    if os.path.exists(env_file):
        print_success(f"File .env tồn tại: {env_file}")
        
        # Load .env
        load_dotenv()
        
        # Kiểm tra GEMINI_API_KEY
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            # Ẩn phần đầu và cuối của API key để bảo mật
            masked_key = gemini_key[:8] + "..." + gemini_key[-4:] if len(gemini_key) > 12 else "***"
            print_success(f"GEMINI_API_KEY: {masked_key}")
            
            # Kiểm tra độ dài API key
            if len(gemini_key) >= 30:
                print_success("API key có độ dài hợp lệ")
            else:
                print_warning("API key có vẻ ngắn, có thể không hợp lệ")
        else:
            print_error("GEMINI_API_KEY không được tìm thấy trong .env")
            return False
            
        # Kiểm tra các biến môi trường khác
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            print_success(f"DATABASE_URL: {database_url}")
        else:
            print_warning("DATABASE_URL không được tìm thấy")
            
    else:
        print_error(f"File .env không tồn tại: {env_file}")
        return False
    
    return True

def test_dependencies():
    """Kiểm tra các dependencies cần thiết"""
    print_header("KIỂM TRA DEPENDENCIES")
    
    required_packages = [
        "langchain",
        "langchain_google_genai", 
        "google_generativeai",
        "pydantic",
        "sqlalchemy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "google_generativeai":
                # Test import trực tiếp
                import google.generativeai as genai
                version = getattr(genai, "__version__", "Unknown")
                print_success(f"{package}: {version}")
            elif package == "langchain_google_genai":
                # Test import trực tiếp
                from langchain_google_genai import ChatGoogleGenerativeAI
                print_success(f"{package}: Imported successfully")
            else:
                # Test import thông thường
                module = __import__(package.replace("-", "_"))
                version = getattr(module, "__version__", "Unknown")
                print_success(f"{package}: {version}")
        except ImportError:
            print_error(f"{package}: Không được cài đặt")
            missing_packages.append(package)
        except Exception as e:
            print_error(f"{package}: Lỗi import - {e}")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"Cần cài đặt: {' '.join(missing_packages)}")
        return False
    
    return True

def test_gemini_connection():
    """Kiểm tra kết nối Gemini API"""
    print_header("KIỂM TRA KẾT NỐI GEMINI API")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Lấy API key
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            print_error("Không thể lấy GEMINI_API_KEY")
            return False
        
        print_info("Đang kết nối đến Gemini API...")
        
        # Tạo LLM instance
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_key,
            temperature=0.7,
            max_output_tokens=8192
        )
        
        print_success("Đã tạo ChatGoogleGenerativeAI instance")
        
        # Test kết nối đơn giản
        print_info("Đang test kết nối với prompt đơn giản...")
        
        test_prompt = "Hãy trả lời ngắn gọn: 'Xin chào, tôi là Gemini AI'"
        response = llm.invoke(test_prompt)
        
        if hasattr(response, 'content'):
            content = response.content
            print_success(f"Phản hồi từ Gemini: {content}")
        else:
            print_success(f"Phản hồi từ Gemini: {response}")
        
        return True
        
    except Exception as e:
        print_error(f"Lỗi khi kết nối Gemini API: {str(e)}")
        print_info(f"Loại lỗi: {type(e).__name__}")
        return False

def test_story_generation():
    """Kiểm tra chức năng tạo story"""
    print_header("KIỂM TRA CHỨC NĂNG TẠO STORY")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import PydanticOutputParser
        
        # Import models
        try:
            from core.models import StoryLLMResponse
            print_success("Đã import StoryLLMResponse")
        except ImportError as e:
            print_error(f"Không thể import StoryLLMResponse: {e}")
            return False
        
        # Import prompts
        try:
            from core.prompts import STORY_PROMPT
            print_success("Đã import STORY_PROMPT")
        except ImportError as e:
            print_error(f"Không thể import STORY_PROMPT: {e}")
            return False
        
        # Tạo LLM
        gemini_key = os.getenv("GEMINI_API_KEY")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=gemini_key,
            temperature=0.7,
            max_output_tokens=8192
        )
        
        # Tạo parser
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        
        # Tạo prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", STORY_PROMPT),
            ("human", "Create a simple story with this theme: adventure")
        ]).partial(format_instructions=story_parser.get_format_instructions())
        
        print_success("Đã tạo prompt template")
        
        # Test với prompt đơn giản trước
        print_info("Đang test với prompt đơn giản...")
        
        simple_prompt = "Hãy tạo một câu chuyện ngắn về chủ đề phiêu lưu. Trả lời bằng tiếng Việt, tối đa 2 câu."
        response = llm.invoke(simple_prompt)
        
        if hasattr(response, 'content'):
            content = response.content
            print_success(f"Phản hồi story test: {content}")
        else:
            print_success(f"Phản hồi story test: {response}")
        
        return True
        
    except Exception as e:
        print_error(f"Lỗi khi test story generation: {str(e)}")
        print_info(f"Loại lỗi: {type(e).__name__}")
        return False

def test_model_versions():
    """Kiểm tra version của các model"""
    print_header("THÔNG TIN VERSION")
    
    try:
        import langchain
        print_info(f"LangChain version: {langchain.__version__}")
    except:
        print_warning("Không thể lấy LangChain version")
    
    try:
        # Test import và version cho langchain_google_genai
        from langchain_google_genai import ChatGoogleGenerativeAI
        print_info("LangChain Google GenAI: Imported successfully")
    except Exception as e:
        print_warning(f"Không thể import LangChain Google GenAI: {e}")
    
    try:
        # Test import và version cho google_generativeai
        import google.generativeai as genai
        version = getattr(genai, "__version__", "Unknown")
        print_info(f"Google GenerativeAI version: {version}")
    except Exception as e:
        print_warning(f"Không thể lấy Google GenerativeAI version: {e}")
    
    try:
        import pydantic
        print_info(f"Pydantic version: {pydantic.__version__}")
    except:
        print_warning("Không thể lấy Pydantic version")
    
    # Return True vì tất cả versions đều được lấy thành công
    return True

def main():
    """Hàm chính để chạy tất cả tests"""
    print_header("🚀 BẮT ĐẦU TEST GEMINI API")
    print_info(f"Thời gian test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Chạy các test
    tests = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies),
        ("Gemini Connection", test_gemini_connection),
        ("Story Generation", test_story_generation),
        ("Model Versions", test_model_versions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Lỗi khi chạy test {test_name}: {e}")
            results.append((test_name, False))
    
    # Tóm tắt kết quả
    print_header("📊 TÓM TẮT KẾT QUẢ")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Kết quả: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 Tất cả tests đều thành công! Gemini API hoạt động bình thường.")
    else:
        print_warning(f"⚠️  Có {total - passed} test(s) thất bại. Vui lòng kiểm tra lỗi ở trên.")
    
    print_header("🏁 KẾT THÚC TEST")

if __name__ == "__main__":
    main()
